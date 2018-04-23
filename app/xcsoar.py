from aerofiles.xcsoar import Writer


def write_xcsoar_task(fp, task):
    writer = Writer(fp)

    params = {
        'type': get_task_type(task),
        'task_scored': 0, #task.task_scored,
        'aat_min_time': 0, #task.aat_min_time,
        'start_max_speed': 0, #task.start_max_speed,
        'start_max_height': 0, #task.start_max_height,
        'start_max_height_ref': 0, #task.start_max_height_ref,
        'finish_min_height': 0, #task.finish_min_height,
        'finish_min_height_ref': 0, #task.finish_min_height_ref,
        'fai_finish': True, #task.fai_finish,
        'min_points': 0, #task.min_points,
        'max_points': 0, #task.max_points,
        'homogeneous_tps': 0, #task.homogeneous_tps,
        'is_closed': True, #task.is_closed,
    }
    print(params)
   
    # Write <Task> tag
    with writer.write_task(**params):

        # Iterate over turnpoints
        #for i, turnpoint in enumerate(task):
        for turnpoint in task.turnpoints:
            print(task.turnpoints)

            # Write <Point> tag
            with writer.write_point(type=get_point_type(task, turnpoint.point_index)):

                # Write <Waypoint> tag
                writer.write_waypoint(
                    name=turnpoint.name,
                    latitude=turnpoint.latitude,
                    longitude=turnpoint.longitude,
                    id=turnpoint.id,
                    comment="", #turnpoint.comment,
                    altitude=turnpoint.elevation,
                )

                # Write <ObservationZone> tag
                #params = get_observation_zone_params(turnpoint.sector)
                # writer.write_observation_zone(**params)
                # writer.write_observation_zone(
                # type=ObservationZoneType.CYLINDER,
                # radius=30000,
                #)

                
                # params = get_observation_zone_params(turnpoint.sector)
                params = get_observation_zone_params(turnpoint)
                print(params)
                writer.write_observation_zone(**params)


def get_task_type(task):
    if task.task_type == 'fai':
        return 'FAIGeneral'
    elif task.task_type == 'triangle':
        return 'FAITriangle'
    elif task.task_type == 'outreturn':
        return 'FAIOR'
    elif task.task_type == 'goal':
        return 'FAIGoal'
    elif task.task_type == 'racing':
        return 'RT'
    elif task.task_type == 'aat':
        return 'AAT'
    elif task.task_type == 'mixed':
        return 'Mixed'
    elif task.task_type == 'touring':
        return 'Touring'


def get_point_type(task, i):
    if i == 0:
        return 'Start'
    elif i == len(task.turnpoints) - 1:
        return 'Finish'
    elif task.task_type == 'aat':
        return 'Area'
    else:
        return 'Turn'


def get_observation_zone_params(turnpoint):
    params = {}

    if turnpoint.oz_line == True:
        print("Recognized Line")
        params["type"] = "Line"
        print(turnpoint.oz_radius1)
        params["length"] = int(turnpoint.oz_radius1) * 2 

    elif turnpoint.type == 'point' and int(turnpoint.oz_angle1) == 180:
        params["type"] = "Cylinder"
        params["radius"] = int(turnpoint.oz_radius1)

    # TODO: Implement FAI turnpoint
    elif turnpoint.type == 'fai':
        params["type"] = "FAISector"

    elif turnpoint.type == 'point' and int(turnpoint.oz_angle1) == 45 and int(turnpoint.oz_angle2) == 180 and turnpoint.oz_radius1 == 10000 and turnpoint.oz_radius2 == 500:
        params["type"] = "Keyhole"

    # TODO: Implement BGAStartSector
    elif turnpoint.type == 'bgastartsector':
        params["type"] = "BGAStartSector"

    # TODO: Implement BGA Fixed Course
    elif turnpoint.type == 'bgafixedcourse':
        params["type"] = "BGAFixedCourse"

    # TODO: Implement BGA Enhanced option
    elif turnpoint.type == 'bgaenhancedoption':
        params["type"] = "BGAEnhancedOption"

    elif turnpoint.type == 'turnpoint':
        params["type"] = "Sector"
        params["radius"] = turnpoint.radius * 1000
        params["start_radial"] = turnpoint.start_radial
        params["end_radial"] = turnpoint.end_radial

        if turnpoint.inner_radius:
            params["inner_radius"] = turnpoint.inner_radius * 1000

    return params