class Case:
    def __init__(self, uuid='', title='', txt_string=''):
        if txt_string:
            self.uuid = txt_string.split("(")[-1].split(")")[0]
            self.title = txt_string.replace(self.uuid, '')[:-2]
        else:
            self.uuid = str(uuid)
            self.title = title
