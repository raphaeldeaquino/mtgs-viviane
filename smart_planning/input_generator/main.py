from shapely.geometry import Polygon
from cl_generator import *
from industry_generator import *
from room_generator import *
from application_generator import *
from info_flow_generator import *
from ifr_flow_generator import *

AREAS = {
    "Production": 0.6,
    "Storage": 0.15,
    "Office": 0.1,
    "Technical Area": 0.1,
    "Common Area": 0.05,
}

industry_coordinates = [(-16.826091, -49.218526),
                        (-16.827192, -49.218437),
                        (-16.827243, -49.218947),
                        (-16.827767, -49.218942),
                        (-16.827798, -49.219392),
                        (-16.826129, -49.219440),
                        (-16.826091, -49.218526)]
industry_polygon = Polygon(industry_coordinates)
room1_coordinates = [(-16.82606883471754, -49.218518735662784),
                     (-16.82609095870916, -49.21946308854425),
                     (-16.826721995232298, -49.21943458131755),
                     (-16.82669450910615, -49.21850242895253),
                     (-16.82606883471754, -49.218518735662784)
                     ]
room1 = Polygon(room1_coordinates)
room2_coordinates = [(-16.82674948135771, -49.21867914029678),
                     (-16.82677273884258, -49.21943237242112),
                     (-16.827178687209535, -49.219423536853675),
                     (-16.827146972524677, -49.21866809583747),
                     (-16.82674948135771, -49.21867914029678)
                     ]
room2 = Polygon(room2_coordinates)
room3_coordinates = [(-16.8267600529421, -49.218442788867726),
                     (-16.8267621672589, -49.21867914029678),
                     (-16.82716388702393, -49.21866146916189),
                     (-16.827159658399257, -49.21843616219215),
                     (-16.8267600529421, -49.218442788867726)
                     ]
room3 = Polygon(room3_coordinates)
room4_coordinates = [(-16.827178687209535, -49.218970714022326),
                     (-16.82718503014587, -49.21942132796182),
                     (-16.82745777620721, -49.21941470128624),
                     (-16.82744086173422, -49.21895966956302),
                     (-16.827178687209535, -49.218970714022326)
                     ]
room4 = Polygon(room4_coordinates)
room5_coordinates = [(-16.827449318981326, -49.218964087347246),
                     (-16.82745989052666, -49.21940807461115),
                     (-16.828005381465243, -49.21939261236813),
                     (-16.82798846704114, -49.218937580644926),
                     (-16.827449318981326, -49.218964087347246)
                     ]
room5 = Polygon(room5_coordinates)
rooms_list = [room1, room2, room3, room4, room5]
candidate_locations_list = generate_candidate_locations(rooms_list)
generate_industry(industry_coordinates, candidate_locations_list)
for i in range(len(rooms_list)):
    generate_room(f"room-0{i + 1}", "industry-01", list(rooms_list[i].exterior.coords))
application_data = generate_applications()
info_flow_data = generate_info_flows(1, application_data)
generate_ifr_flows(3, info_flow_data)
