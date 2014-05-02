from revengeapp.models import revengePoint


def get_revenge_points(request):
    revPoints = revengePoint.objects.all()
    return {'revPoints': revPoints}
