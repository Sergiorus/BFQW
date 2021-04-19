class DataHolder:
    def __init__(self, picture_path='/picr.png', source_data='', current_data=''):
        self.picture_path = picture_path
        self.source_data = source_data
        self.current_data = current_data


    def update_values(self, picture_path = None, source_data = None, current_data = None):
        if picture_path:
            self.picture_path = picture_path
        if source_data:
            self.source_data = source_data
        if current_data:
            self.current_data = current_data