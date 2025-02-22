from celery import shared_task
from pathfinder_server.celery import app
from .models import (
    RtImage,
    AiModel,
    AiDefect,
)
from .serializers import (
    AiModelCreateSerializer,
    AiDefectSerializer,
)
from .ai.ai_process import ai_model_efficientdet


@shared_task
def computer_vision_process_task(rt_image_id: int):
    """Get result from ai model and save to db"""

    defect_name = {
        1 : 'others',
        2 : 'porosity',
        3 : 'slag',
    }

    rt_image = RtImage.objects.get(pk=rt_image_id)

    # ai단 함수 호출
    defect_data_set_dict = ai_model_efficientdet(rt_image.image.path)

    box_set = defect_data_set_dict['boxes']
    defect_score_set = defect_data_set_dict['scores']
    defect_type_set = defect_data_set_dict['labels']

    # 결함이 없어도 반드시 추가할 것
    ai_model_serializer = AiModelCreateSerializer(
        data={'rt_image' : rt_image_id}
    )
    if ai_model_serializer.is_valid():
        ai_model_serializer.save()
    else:
        print(ai_model_serializer.errors)
        return

    # 결함이 있을 경우에만 사용할 것
    for defect_type, score, box in zip(defect_type_set, defect_score_set, box_set):
        if score < 0.1:
            continue
        defect_serializer = AiDefectSerializer(
            data={
                'ai_model'      : ai_model_serializer.data['pk'],
                'defect_type'   : defect_name[int(defect_type)],
                'score'         : float(score),
                'xmin'          : float(box[0][0]),
                'ymin'          : float(box[0][1]),
                'xmax'          : float(box[0][2]),
                'ymax'          : float(box[0][3]),
            })
        if defect_serializer.is_valid():
            defect_serializer.save()
        else:
            print(defect_serializer.errors)
            return
    print("Finished AI model task")
    return 