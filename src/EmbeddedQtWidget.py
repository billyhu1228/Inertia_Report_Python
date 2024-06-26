from queue import Full
from Qt import QtCore, QtWidgets # type: ignore
from NodeGraphQt import NodeGraph, BaseNode,NodeBaseWidget,NodesPaletteWidget,BaseNodeCircle
from NodeGraphQt.constants import PipeLayoutEnum
import catia
from catia.catia import CatiaApp
import json
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF, QPointF




# Print the dummy data to verify the structure
#print(json.dumps(DefaultDummyData, indent=2))



# class MyCustomWidget(QtWidgets.QWidget):
#     """
#     Custom widget to be embedded inside a node.
#     """

#     def __init__(self, parent=None):
#         super(MyCustomWidget, self).__init__(parent)
        
#         # Initialize QLineEdit widgets for Mass inputs
#         self.mass_nominal = QtWidgets.QLineEdit()
#         self.mass_min = QtWidgets.QLineEdit()
#         self.mass_max = QtWidgets.QLineEdit()

#         # Setup placeholders to improve user experience
#         self.mass_nominal.setPlaceholderText("Mass (Nominal)")
#         self.mass_min.setPlaceholderText("Mass (Min)")
#         self.mass_max.setPlaceholderText("Mass (Max)")

#         # Button to trigger actions
#         self.btn_go = QtWidgets.QPushButton('Detail')

#         # Create layout and add widgets
#         layout = QtWidgets.QHBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.addWidget(self.mass_nominal)
#         layout.addWidget(self.mass_min)
#         layout.addWidget(self.mass_max)
#         layout.addWidget(self.btn_go)


# class NodeWidgetWrapper(NodeBaseWidget):
#     """
#     Wrapper that allows the widget to be added in a node object.
#     """

#     def __init__(self, parent=None):
#         super(NodeWidgetWrapper, self).__init__(parent)
        
#         # set the name for node property.
#         self.set_name('Mass Specifications (Kg)')
        
#         # set the label above the widget.
#         self.set_label('Mass Specs (kg)')
        
#         # set the custom widget.
#         self.set_custom_widget(MyCustomWidget())
        
#         # connect up the signals & slots.
#         self.wire_signals()

#     def wire_signals(self):
#         widget = self.get_custom_widget()
        
#         # wire up the QLineEdit widgets for live updates or validation
#         widget.mass_nominal.textChanged.connect(self.on_value_changed)
#         widget.mass_min.textChanged.connect(self.on_value_changed)
#         widget.mass_max.textChanged.connect(self.on_value_changed)
        
#         # wire up the button.
#         widget.btn_go.clicked.connect(self.on_btn_go_clicked)

#     def on_btn_go_clicked(self):
#         print('Clicked on node: "{}"'.format(self.node.name()))

#     def get_value(self):
#         widget = self.get_custom_widget()
#         return '{}/{}/{}'.format(widget.mass_nominal.text(),
#                                  widget.mass_min.text(),
#                                  widget.mass_max.text())

#     def set_value(self, value):
#         parts = value.split('/')
#         widget = self.get_custom_widget()
#         if len(parts) == 3:
#             widget.mass_nominal.setText(parts[0])
#             widget.mass_min.setText(parts[1])
#             widget.mass_max.setText(parts[2])


# class MyNode(BaseNode):
#     """
#     Example node.
#     """

#     # set a unique node identifier.
#     __identifier__ = 'io.github.jchanvfx'

#     # set the initial default node name.
#     NODE_NAME = 'Inertia'

#     def __init__(self):
#         super(MyNode, self).__init__()

#         node_widget = NodeWidgetWrapper(self.view)
#         self.add_custom_widget(node_widget, tab='Custom')






class MassDetailsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MassDetailsDialog, self).__init__(parent)
        self.setWindowTitle("Mass Details")
        
        # Initialize QLineEdit widgets for Mass inputs
        self.mass_nominal = QtWidgets.QLineEdit()
        self.mass_min = QtWidgets.QLineEdit()
        self.mass_max = QtWidgets.QLineEdit()

        # Set up placeholders to guide the user
        self.mass_nominal.setPlaceholderText("Enter Nominal Mass")
        self.mass_min.setPlaceholderText("Enter Minimum Mass")
        self.mass_max.setPlaceholderText("Enter Maximum Mass")

        # Layout setup
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.mass_nominal)
        layout.addWidget(self.mass_min)
        layout.addWidget(self.mass_max)

        # Buttons for OK and Cancel
        btn_ok = QtWidgets.QPushButton("OK")
        btn_cancel = QtWidgets.QPushButton("Cancel")
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        layout.addWidget(btn_ok)
        layout.addWidget(btn_cancel)

    def get_values(self):
        return (self.mass_nominal.text(), self.mass_min.text(), self.mass_max.text())

    def set_values(self, nominal, minimum, maximum):
        self.mass_nominal.setText(nominal)
        self.mass_min.setText(minimum)
        self.mass_max.setText(maximum)


class MyCustomWidget(QtWidgets.QWidget):
    """
    Custom widget containing a single button.
    """
    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        self.bodyBtn = QtWidgets.QPushButton()  # Remove text if not needed
        icon = QtGui.QIcon("Inertia_Report_Python/src/resource/icons8-search-100.pngsrc/resource/icons8-search-100.png")  # Update the path to your icon
        self.bodyBtn.setIcon(icon)
        #self.btn_go.setIconSize(QtGui.QSize(32, 32))  # Optional: Adjust size as needed
        
           # Initialize the additional details widget but don't add to layout yet
        self.massDetail = QtWidgets.QLabel("Additional Details Here")
       
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.bodyBtn)

   
        


          # Second button setup
        self.springBtn = QtWidgets.QPushButton()
        icon_second = QtGui.QIcon("src/resource/icons8-coil-50.png")  # Update the path to your second icon
        self.springBtn.setIcon(icon_second)
        layout.addWidget(self.springBtn)
        #self.springBtn.setIconSize(QtGui.QSize(32, 32))  # Optional: Adjust size as needed

        self.MassDetails_visible = False  # Track visibility state





class NodeWidgetWrapper(NodeBaseWidget):
    def __init__(self, parent=None):
        super(NodeWidgetWrapper, self).__init__(parent)
        self.set_custom_widget(MyCustomWidget())
        self.wire_signals()

    def wire_signals(self):
        widget = self.get_custom_widget()
        widget.bodyBtn.clicked.connect(self.on_BodyDetailClick)
        widget.springBtn.clicked.connect(self.on_SpringDetailClick)

    def on_BodyDetailClick(self):
        print('Clicked on node: "{}"'.format(self.node.name()))
        dialog = MassDetailsDialog()



      



        #First Check from the DummyDate to see if there is mass in there 

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            nominal, minimum, maximum = dialog.get_values()
            print(f"Mass details saved: Nominal={nominal}, Min={minimum}, Max={maximum}")
         # Here you can handle the values, such as saving them or updating the node



    def on_SpringDetailClick(self):
        print('Clicked on node: "{}"'.format(self.node.name()))










    def get_value(self):
        # Instead of raising NotImplementedError, return a dummy value.
        # Return a value that represents the state of your widget if applicable.
        # Since the widget only has a button, you might just return an empty string or None.
        return ""

    def set_value(self, value):
        # For now, do nothing or you can log the value if needed
        # Implement this method to set the widget's state if necessary
        pass




class MyNode(BaseNode):
    """
    Example node.
    """

    # set a unique node identifier.
    __identifier__ = 'io.github.jchanvfx'

    # set the initial default node name.
    NODE_NAME = 'Body'

    def __init__(self):
        super(MyNode, self).__init__()

        node_widget = NodeWidgetWrapper(self.view)
        self.add_custom_widget(node_widget, tab='Custom')


class MyCircleNode(BaseNodeCircle):
    """
    Example node.
    """

   # unique node identifier domain.
    __identifier__ = 'io.jchanvfx.github'

    # initial default node name.
    NODE_NAME = 'Cable'

    def __init__(self):
        super(MyCircleNode, self).__init__()




























def draw_triangle_port(painter, rect, info):
    painter.save()
    size = int(rect.height() / 2)
    triangle = QtGui.QPolygonF()
    triangle.append(QtCore.QPointF(-size, size))
    triangle.append(QtCore.QPointF(0.0, -size))
    triangle.append(QtCore.QPointF(size, size))
    transform = QtGui.QTransform()
    transform.translate(rect.center().x(), rect.center().y())
    port_poly = transform.map(triangle)

    color = QtGui.QColor(*info['color']) if not info['hovered'] else QtGui.QColor(255, 255, 0)
    border_color = QtGui.QColor(*info['border_color'])

    pen = QtGui.QPen(border_color, 2)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)
    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawPolygon(port_poly)
    painter.restore()



def map_bodies_to_axes(bodies, axes):
    mapping = {}
    unmatched_bodies = set(bodies)  # Start with all bodies as unmatched

    for axis in axes:
        axis_name = axis['Name']
        mapping[axis_name] = []  # Initialize each axis entry as an empty list
        for body in bodies:
            if body in axis_name:
                mapping[axis_name].append(body)  # Append the body to the list for this axis
                unmatched_bodies.discard(body)  # Remove matched body from unmatched set

    # Remove empty lists: only if you do not want to keep axes with no matched bodies
    for key in list(mapping.keys()):
        if not mapping[key]:
            del mapping[key]

    return mapping, list(unmatched_bodies)
    

def connect_bodies_within_backdrops(backdrops):
    
    for backdrop in backdrops:
        if len(backdrop.bodies) > 1:
            # Connect bodies within the same backdrop
            previous_body = None
            for body in backdrop.bodies:
                if previous_body:
                    graph.connect_nodes(previous_body, body)
                previous_body = body

def generate_force_mappings(data):
    force_mappings = []

    for item in data:
        name = item['Name']
        
        # Check if '2' is present in the name
        if '2' not in name:
            raise ValueError(f"Invalid force name format: {name}")
        
        parts = name.split('2')
        
        # Extract start and end points from the name
        start = parts[0]
        end = parts[1].split('_')[0]  # Clean the end name

        force_mapping = {
            "force_name": name,
            "start": start,
            "end": end,
            "P1": item['P1'],
            "P2": item['P2'],
            "ForceType": "push"
        }
        
        force_mappings.append(force_mapping)
    
    force_mappings_json = json.dumps({"force_mappings": force_mappings}, indent=2)
    #print(force_mappings_json)
    return force_mappings


def add_ForcesForDefaultAxis(catia_app: CatiaApp, DefaultDummyData):
    get_points_forces_cables = catia_app.get_points_forces_cables("Forces")


    force_maps = generate_force_mappings(get_points_forces_cables)

    #print(json.dumps(force_maps, indent=2))


    #print(DefaultDummyData["AxisSystem"])

    #print(json.dumps(DefaultDummyData["AxisSystem"], indent=2))


  

    for Axis in DefaultDummyData["AxisSystem"]:
        axisName = Axis["AxisSystem_Name"]
        for body in Axis["Bodies"]: 

            for force in force_maps:
                start = force['start']
                end= force['end']
                forcename= force['force_name']
                
                #print( "Axis: "+ axisName + "--->     Body " + body["name"] + " ---> Force : "+ start  )
                if body["name"] == start:
                     print( "Axis: "+ axisName + "--->     Body " + body["name"] + " ---> Force : "+ forcename  )
                
                     if "OutForces" not in body:
                         body["OutForces"] = []
                     # Check if the force is already in the list before appending
                     if not any(f["force_name"] == force["force_name"] for f in body["OutForces"]):
                         body["OutForces"].append(force)
                
                if body["name"] == end:
                    print("Axis: " + axisName + " ---> Body " + body["name"] + " ---> IncomingForce: " + forcename)
                    if "InForces" not in body:
                        body["InForces"] = []
                    # Check if the force is already in the list before appending
                    if not any(f["force_name"] == force["force_name"] for f in body["InForces"]):
                        body["InForces"].append(force)

    
   # Then handle forces associated with cables
    for cable in DefaultDummyData["Cables"]:
        cableName = cable["CableName"]
        
        for force in force_maps:
            start = force['start']
            end = force['end']
            forcename = force['force_name']
            
            # Allocate outgoing forces to cables
            if cableName == start:
                
                cable["OutForces"].append(force)
                print(f"######### Cable: {cableName} ---> Outgoing Force: {forcename}")
            
        
    return DefaultDummyData
     

def add_CablesSystem(catia_app: CatiaApp, DefaultDummyData):
    get_points_forces_cables = catia_app.get_points_forces_cables("Cables")

    # Update Object based on this API
    print(get_points_forces_cables)

    for cable in get_points_forces_cables:
        cable_name = cable['Name']
        p1 = cable['P1']
        p2 = cable['P2']

        # Check if the cable already exists in DefaultDummyData
        for existing_cable in DefaultDummyData['Cables']:
            if existing_cable['CableName'] == cable_name:
                # Update existing cable data
                existing_cable['p1']['x'], existing_cable['p1']['y'], existing_cable['p1']['z'] = p1
                existing_cable['p2']['x'], existing_cable['p2']['y'], existing_cable['p2']['z'] = p2
                break
        else:
            # If cable does not exist, add new cable
            DefaultDummyData['Cables'].append({
                "CableName": cable_name,
                "mass": {
                    "max": 0,
                    "nominal": 0,
                    "min": 0
                },
                "length": 0,
                "p1": {
                    "x": p1[0],
                    "y": p1[1],
                    "z": p1[2]
                },
                "p2": {
                    "x": p2[0],
                    "y": p2[1],
                    "z": p2[2]
                },
                "OutForces": [

                ]
            })

    return DefaultDummyData



def add_AxisSystem(catia_app: CatiaApp, DefaultDummyData):
    axis_systems = catia_app.get_displayed_axis_systems()

    for axis in axis_systems:
        found = False  # Flag to track if the axis system is found

        for existing_axis in DefaultDummyData["AxisSystem"]:
            if existing_axis["AxisSystem_Name"] == axis['Name']:
                # Update the AxisCoordination for the existing entry
                existing_axis["AxisCoordination"] = {
                    "origin": axis['Origin'],
                    "transformation matrix": [
                        axis['X_Axis'],
                        axis['Y_Axis'],
                        axis['Z_Axis']
                    ]
                }
                found = True
                break  # Stop searching once the axis system is found and updated

        if not found:
            # Create new axis system entry if not found
            new_axis_system = {
                "AxisSystem_Name": axis['Name'],
                "AxisCoordination": {
                    "origin": axis['Origin'],
                    "transformation matrix": [
                        axis['X_Axis'],
                        axis['Y_Axis'],
                        axis['Z_Axis']
                    ]
                },
                "Bodies": []  # Start with an empty list of bodies
            }
            DefaultDummyData["AxisSystem"].append(new_axis_system)

    return DefaultDummyData


def add_Bodies_Cog(catia_app: CatiaApp, DefaultDummyData):
    # Retrieve the COGs of displayed bodies
    get_displayed_body_cog = catia_app.get_displayed_body_cog()

    # Loop through each Axis System in DefaultDummyData
    for axis_system in DefaultDummyData["AxisSystem"]:
        # Loop through each body in the current Axis System
        for body in axis_system["Bodies"]:
            body_name = body["name"]  # Get the name of the body
            # Check if the body name is in the COG data retrieved
            if body_name in get_displayed_body_cog:
                # Update the COG coordinates of the body
                body["COG"]["coordinates"] = get_displayed_body_cog[body_name]
            else:
                # If no COG data is available, set coordinates to None or keep existing data
                body["COG"]["coordinates"] = body.get("COG", {}).get("coordinates", None)

    return DefaultDummyData






def setup_and_connect_nodes(graph, DefaultDummyData, initial_y=100):
    node_dict = {}  # To store created nodes with their names as keys
    initial_x = 200
    unnamed_initial_y = initial_y  # Separate y-coordinate for bodies without a named axis system
    x_offset = -800  # Distance to place cable nodes to the left of the body node
    ####### Draw the diagram for the cable
    
    for cable  in DefaultDummyData["Cables"]:
        cableName = cable["CableName"]
        cableNode = graph.create_node('io.jchanvfx.github.MyCircleNode', name=cableName, 
                                              pos=(initial_x+ x_offset, initial_y) , 
                                              text_color='#FFFFFF')
        for force in cable.get("OutForces", []):
                    out_port_name = f"Out - {force['force_name']}"
                    cableNode.add_output(out_port_name)
        
         # Add the created node to node_dict
        node_dict[cableName] = cableNode

        






    ##### Draw The Diagram for the Axis system 
    for data in DefaultDummyData["AxisSystem"]:
        axis_system_name = data["AxisSystem_Name"]
        nodes_in_backdrop = []  # To store nodes that will be wrapped by the backdrop
        
        # Determine the vertical position based on whether the axis system has a name
        current_y = initial_y if axis_system_name else unnamed_initial_y

        if axis_system_name:
            # Create a backdrop for named axis systems
            axis_backdrop = graph.create_node('nodeGraphQt.nodes.BackdropNode', name=axis_system_name, pos=(initial_x, current_y))

        node_y_offset = 0  # Incremental offset for nodes within the same backdrop
        for body in data["Bodies"]:
            number_of_Outforces = len(body.get("OutForces", []))
            number_of_Inforces = len(body.get("InForces", [])) 

            if body["name"]:
                body_name = body["name"]
                # Adjust node position within backdrop based on offset
                body_node = graph.create_node('io.github.jchanvfx.MyNode', name=body_name, 
                                              pos=(initial_x, current_y + node_y_offset), 
                                              text_color='#FFFFFF')
                node_dict[body_name] = body_node  # Store the node reference

                nodes_in_backdrop.append(body_node)  # Add to backdrop if part of a named system

        
                # Add input and output ports
                for inforce in body.get("InForces", []):
                    #in_port_name = f"IN - {inforce['force_name']}"
                    in_port_name = f"IN -"
                    body_node.add_input(in_port_name, painter_func=draw_triangle_port)
                

                for force in body.get("OutForces", []):
                    #out_port_name = f"Out - {force['force_name']}"
                    out_port_name = f"Out -"
                    body_node.add_output(out_port_name)

                # Adjust vertical position for next node
                node_y_offset += 200  # Adjust spacing per node

        if axis_system_name and nodes_in_backdrop:
            axis_backdrop.wrap_nodes(nodes_in_backdrop)
            # Reset initial_y below the backdrop for the next set of nodes or backdrops
            initial_y = max(current_y + node_y_offset + 100, unnamed_initial_y)  # Ensure spacing after the last backdrop

    # Context menu addition, seems misplaced here, ensure this is intended to be within the function
    nodes_menu = graph.get_context_menu('nodes')
    nodes_menu.add_command('Test', func=lambda: print("Test function executed"), node_type='io.github.jchanvfx.MyNode')

    print(node_dict)

    # Connect nodes based on forces
    for data in DefaultDummyData["AxisSystem"]:
        for body in data["Bodies"]:
            body_name = body["name"]
            body_node = node_dict.get(body_name)
            for force in body.get("OutForces", []):
                start_node = node_dict.get(force["start"])
                end_node = node_dict.get(force["end"])
                if start_node and end_node:
                    start_node.set_output(0, end_node.input(0))



   
    # Connect the cable to the body based on OutForces
    for cable in DefaultDummyData["Cables"]:
        cableName = cable["CableName"]
        cableNode = node_dict.get(cableName)  # Retrieve the cable node from node_dict
    
        if "OutForces" in cable:
            for force in cable["OutForces"]:
                targetName = force['end']  # The name of the node this cable should connect to
                targetNode = node_dict.get(targetName)  # Retrieve the target node from node_dict
    
                if cableNode and targetNode:
                    # Connect the first output of the cable node to the first input of the target node
                    cableNode.set_output(0, targetNode.input(0))

                    #graph.connect_ports(cableNode.outputs[0], targetNode.inputs[0])
                    print(f"Connected {cableName} to {targetName}")
                else:
                    if not cableNode:
                        print(f"Warning: Cable node named '{cableName}' not found.")
                    if not targetNode:
                        print(f"Warning: Target node named '{targetName}' not found.")





  


    

    return graph


    
# define a test function.
def test_func(graph, node):
    print('Clicked on node: {}'.format(node.name()))   
    





if __name__ == '__main__':

    

    app = QtWidgets.QApplication([])

    

    catia = catia.CatiaApp()
    catia.get_active_doc()

    AxisBody_map =  map_bodies_to_axes(catia.get_displayed_body_names(), catia.get_displayed_axis_systems())

    print(json.dumps( AxisBody_map, indent=2))
 


    axis_systems = []

# Loop through each axis and associated bodies from AxisBody_map[0]
    for axis_name, bodies in AxisBody_map[0].items():
        # Prepare a list of body dictionaries for this axis
        body_details = [
            {
                "name": body,
                "mass": {"Nominal": "", "Minimum": "", "Maximum": ""},
                "COG": {"coordinates": []},
                "Spring": {
                    "name": "example_spring",
                    "stiffness": 0.0,
                    "rls_angle": 0.0,
                    "moment_arm_ratio": 0.0,
                    "installed_torque": 0.0,
                    "SpringType": ""
                },
                "OutForces": [],
                "InForces": []
            }
            for body in bodies  # Assuming bodies is a list of body names
        ]

        # Append the axis system details into the axis_systems list
        axis_systems.append({
            "AxisSystem_Name": axis_name,
            "AxisCoordination": {
                "origin": [124.1, 4541.5, 454],
                "transformation matrix": [[1.1, 2.2, 3.3], [4.4, 5.5, 6.6], [7.7, 8.8, 9.9]]
            },
            "Bodies": body_details
        })

# Add unique AxisSystem entries for each body listed in AxisBody_map[1]
    # for body_name in AxisBody_map[1]:
    #     axis_systems.append({
    #         "AxisSystem_Name": "",  # No specific name for the axis system
    #         "AxisCoordination": None,  # No coordination data
    #         "Bodies": [
    #             {
    #                 "name": body_name,
    #                 "mass": {"Nominal": "", "Minimum": "", "Maximum": ""},
    #                 "COG": {"coordinates": []},
    #                 "Spring": {
    #                     "name": "example_spring",
    #                     "stiffness": 0.0,
    #                     "rls_angle": 0.0,
    #                     "moment_arm_ratio": 0.0,
    #                     "installed_torque": 0.0,
    #                     "SpringType": ""
    #                 },
    #                 "OutForces": [],
    #                 "InForces": []
    #             }
    #         ]
    #     })

    DefaultDummyData = {
    "Cables": [
        {
            "CableName": "IsRelCable",
            "mass": {"max": 0, "nominal": 0, "min": 0},
            "length": 0,
            "p1": {"x": 0.0, "y": 0.0, "z": 0.0},
            "p2": {"x": 0.0, "y": 0.0, "z": 0.0},
            "OutForces":[]
        }
    ],
    "AxisSystem": axis_systems
}

   
    
   
    #print(json.dumps( DefaultDummyData, indent=2))

    # Constants for grid layout
    initial_y = 50 


    DummyData = add_Bodies_Cog(catia,add_CablesSystem(catia,add_ForcesForDefaultAxis(catia,add_AxisSystem(catia, DefaultDummyData))))
   

    print(json.dumps( DummyData, indent=2))
    
    # create node graph controller.
    graph = NodeGraph()

    # register the  node class.
    graph.register_nodes([MyNode,MyCircleNode])
    


    print("Registered Nodes:", graph.registered_nodes())

   


    graph = setup_and_connect_nodes(graph, DummyData,initial_y=100)

     # show the node graph widget.
    graph_widget = graph.widget
    graph_widget.show()



    









    app.exec_()
