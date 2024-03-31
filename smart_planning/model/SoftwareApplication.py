class SoftwareApplication:

    def __init__(self, app_dict):
        try:
            if app_dict["type"] != "SoftwareApplication":
                raise ValueError("Invalid app dictionary: 'type' must be 'SoftwareApplication'")

            self.id = app_dict["id"]
            self.type = "SoftwareApplication"
            self.description = app_dict["description"] if "description" in app_dict else None
            self.applicationCategory = app_dict["applicationCategory"] if "applicationCategory" in app_dict else None
            self.featureList = app_dict["featureList"] if "featureList" in app_dict else None
            self.memoryRequirements = app_dict["memoryRequirements"] if "memoryRequirements" in app_dict else None
            self.processorRequirements = app_dict["processorRequirements"] if "processorRequirements" in app_dict else None
            self.storageRequirements = app_dict[
                "storageRequirements"] if "storageRequirements" in app_dict else None
            self.softwareRequirements = app_dict[
                "softwareRequirements"] if "softwareRequirements" in app_dict else None
        except KeyError:
            raise ValueError("Invalid software application dictionary")

    def __str__(self):
        # Construindo a representação em string do objeto SoftwareApplication
        app_str = f"Room ID: {self.id}\n"
        app_str += f"Description: {self.description}\n"
        app_str += f"Application category: {self.applicationCategory}\n"
        app_str += f"Feature list: {self.featureList}\n"
        app_str += f"Memory requirements: {self.memoryRequirements}\n"
        app_str += f"Processor requirements: {self.processorRequirements}\n"
        app_str += f"Storage requirements: {self.storageRequirements}\n"
        app_str += f"Software requirements: {self.softwareRequirements}\n"

        return app_str
