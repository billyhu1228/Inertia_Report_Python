from pycatia import catia

class CatiaApp:
    def __init__(self):
        self.caa = catia()

    def get_active_doc(self):
        cat_documents = self.caa.documents
        if cat_documents.count > 0:
            return self.caa.active_document
        else:
            print("CATIA document not opened.")
            return None
        
    def get_active_doc_name(self):
        cat_documents = self.caa.documents
        if cat_documents.count > 0:
            return self.caa.active_document.name
        else:
            print("CATIA document not opened.")
            return None

    def get_displayed_body_names(self):
        active_doc = self.get_active_doc()

        if active_doc:
            part_doc = active_doc.part
            bodies = part_doc.bodies

            displayed_body_names = []

            selection = active_doc.selection
            selection.clear()

            for body in bodies:
                selection.clear()
                selection.add(body)
                show = selection.vis_properties.get_show()

                if show == 0 and body.name != "PartBody":
                    displayed_body_names.append(body.name)

                selection.clear()

            return displayed_body_names

    def get_displayed_axis_systems(self):
        active_doc = self.get_active_doc()

        if active_doc:
            part_doc = active_doc.part
            axis_systems = part_doc.axis_systems

            displayed_axis_systems_data = []

            selection = active_doc.selection
            selection.clear

            for axis_system in axis_systems:
                selection.clear()
                selection.add(axis_system)
                show = selection.vis_properties.get_show()

                if show == 0:
                    origin = axis_system.get_origin()
                    x_axis = axis_system.get_x_axis()
                    y_axis = axis_system.get_y_axis()
                    z_axis = axis_system.get_z_axis()

                    axis_system_data = {
                        "Name": axis_system.name,
                        "Origin": origin,
                        "X_Axis": x_axis,
                        "Y_Axis": y_axis,
                        "Z_Axis": z_axis,
                    }

                    displayed_axis_systems_data.append(axis_system_data)

                selection.clear()

            return displayed_axis_systems_data

    def get_coordinates_of_point(self, point):
        # print(point)
        active_doc = self.get_active_doc()
        part_doc = active_doc.part

        spa_workbench = active_doc.spa_workbench()
        reference = part_doc.create_reference_from_object(point)
        # print(reference)
        measurable = spa_workbench.get_measurable(reference)
        coordinates = measurable.get_point()
        

        # Try to get the COG if applicable
        cog = None
        try:
            cog = measurable.get_cog()
        except Exception as e:
            print(f"Unable to get COG for this object: {e}")

        # print(coordinates)
        return coordinates

    def get_points_forces_cables(self, type):
        
        active_doc = self.get_active_doc()

        if active_doc:
            part_doc = active_doc.part
            hy_body = part_doc.hybrid_bodies.item(type)

            if hy_body:
                bodies_list = hy_body.hybrid_bodies

                points_list = []

                for body in bodies_list:
                    selection = active_doc.selection
                    selection.clear()
                    selection.add(body)
                    show = selection.vis_properties.get_show()

                    if show == 0:
                        name = body.name
                        pointP1 = body.hybrid_shapes.get_item("P1")
                        pointP2 = body.hybrid_shapes.get_item("P2")

                        coordinatesP1 = self.get_coordinates_of_point(pointP1)
                        coordinatesP2 = self.get_coordinates_of_point(pointP2)
                        
                        #print(coordinatesP2)
                        points_list.append({
                            "Name": name,
                            "P1": coordinatesP1,
                            "P2": coordinatesP2
                        })

                    selection.clear()

                return points_list
            else:
                print(f"Hybrid body {type} not found.")
                return None


    def get_displayed_body_cog(self):
        active_doc = self.get_active_doc()

        if active_doc:
            part_doc = active_doc.part
            bodies = part_doc.bodies
    
            displayed_body_cog = {}
    
            selection = active_doc.selection
            selection.clear()
    
            for body in bodies:
                selection.clear()
                selection.add(body)
                show = selection.vis_properties.get_show()
    
                # Check if the body is displayed and not named "PartBody"
                if show == 0 and body.name != "PartBody":
                    spa_workbench = active_doc.spa_workbench()
                    reference = part_doc.create_reference_from_object(body)
                    measurable = spa_workbench.get_measurable(reference)
    
                    try:
                        cog = measurable.get_cog()
                        displayed_body_cog[body.name] = cog
                    except Exception as e:
                        print(f"Unable to get COG for {body.name}: {e}")
                        displayed_body_cog[body.name] = None
    
                selection.clear()
    
            return displayed_body_cog
