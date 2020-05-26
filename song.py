"""..."""


# TODO: Create your Song class in this file


class Song:
    def __init__(self, title='', artist='', year=0, learned=False):
        self.title = title
        self.artist = artist
        self.year =  int(year)
        self.is_learned = learned

    def is_learned(self):
        return self.is_learned

    def mark_learned(self):
        if self.is_learned == False:
            self.is_learned = True
        return self


    def __eq__(self, btn_id):
        equal_check = '{}_{}'.format(self.title, self.year)
        result = (btn_id == equal_check)
        return result

    def __str__(self):
        learn_status = ''
        if self.is_learned == True:
            learn_status = '(learned)'
        return 'Song Details:\n {}\n {}\n {}\n Status: {}'.format(self.title, self.artist, self.year, learn_status)
        #return '{} by {} ({}) {}'.format(self.title, self.artist, self.year, learn_status)



