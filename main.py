"""
Name:
Date:
Brief Project Description:
GitHub URL:
"""
# TODO: Create your main program in this file, using the SongsToLearnApp class


from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from song import Song
from songcollection import SongCollection
import sys


class SongsToLearnApp(App):

    current_selection = StringProperty()
    spinner_menu = ListProperty()
    songs = SongCollection()
    song = Song()
    song_id_list = []

    def build(self):
        SongCollection() # initialise an empty list on program start
        Window.size = (900, 600)
        self.title = 'Songs to Learn 2.0'
        self.root = Builder.load_file('app.kv')
        songs_list = self.load_songs()
        self.create_entry_grids(songs_list)
        self.root.ids.message_box.text = 'Welcome to Songs to Learn 2.0'

        return self.root

    def create_entry_grids(self, input_list):
        self.clear_widget()
        for song in input_list:
            if song.is_learned == True:
                learn_state = '(Learned)'
                btn_color = (0, 1, 0, 1)
            else:
                learn_state = ''
                btn_color = (1, 0, 0, 1)
            btn_id = '{}_{}'.format(song.title, song.year)
            temp_button = Button(id = btn_id, background_color = btn_color,
                text = '"{}" by {} ({}) {}'.format(song.title, song.artist, song.year, learn_state))
            self.root.ids.song_count.add_widget(temp_button)
            self.song_id_list.append(temp_button)
            temp_button.bind(on_release = self.handle_mark)
        self.song_status()


    def handle_clear(self):
        # Clears the text input fields to empty
        self.root.ids.input_title.text = ''
        self.root.ids.input_artist.text = ''
        self.root.ids.input_year.text = ''

    def handle_add(self):
        """Validates input, and passes the inputs to the function to create a new song object"""
        song_title = self.root.ids.input_title.text
        song_artist = self.root.ids.input_artist.text
        song_year = self.root.ids.input_year.text
        err_check = self.error_check()

        if err_check == 'Blank':
            self.root.ids.message_box.color = (1, 0, 0, 1)
            self.root.ids.message_box.text = 'All fields must be completed'
            self.root.ids.btn_add.background_color = (1, 0, 0, 1)
        elif err_check == 'Invalid':
            self.root.ids.message_box.color = (1, 0, 0, 1)
            self.root.ids.message_box.text = 'Year Invalid. Please enter Valid year (1800 to 2018)'
            self.root.ids.btn_add.background_color = (1, 0, 0, 1)
        elif err_check == 'Type':
            self.root.ids.message_box.color = (1, 0, 0, 1)
            self.root.ids.message_box.text = 'Error in Field "Year". Please Check Input'
            self.root.ids.btn_add.background_color = (1, 0, 0, 1)
        elif err_check == 'Duplicate':
            self.root.ids.message_box.color = (1, 0, 0, 1)
            self.root.ids.message_box.text = '{} by {} already exists'.format(song_title, song_artist)
            self.root.ids.btn_add.background_color = (1, 0, 0, 1)
        else:
            send_input = Song(song_title, song_artist, song_year, False)
            # Registers the song attribute given by the user, with additional attribute 'learned' automatically set to False
            added_list = self.songs.add_songs(send_input)
            self.make_entries(added_list)
            self.root.ids.message_box.color = (1, 1, 1, 1)
            self.root.ids.message_box.text = 'You added {} by {}'.format(song_title, song_artist)
            self.root.ids.btn_add.background_color = (0, 0, 1, 1)

    def handle_sort_change(self, spinner_choice):
        self.clear_widget()
        sort_attr = spinner_choice
        if sort_attr == 'Title':
            sorted_list = self.songs.sort_songs(0)
        elif sort_attr == 'Artist':
            sorted_list = self.songs.sort_songs(1)
        elif sort_attr == 'Year':
            sorted_list = self.songs.sort_songs(2)
        self.make_entries(sorted_list)
        self.root.ids.message_box.text = 'Sorted by {}'.format(sort_attr)

    def load_songs(self):
        sort_list = self.songs.load_songs('songs.csv')
        return sort_list

    def song_status(self):
        learn = self.songs.calculate_song_learned()
        not_learn = self.songs.calculate_song_not_learned()
        total_songs = learn + not_learn
        status_text = 'To learn:{}.is_learned:{}'.format( learn, not_learn)
        self.root.ids.status_bar.text = status_text

    def make_entries(self, input_list):
        self.clear_widget()
        for song in input_list:
            if song.is_learned == True:
                learn_state = '(Learned)'
                btn_color = (0, 1, 0, 1)
            else:
                learn_state = ''
                btn_color = (1, 0, 0, 1)
            btn_id = '{}_{}'.format(song.title, song.year)
            temp_button = Button(id = btn_id, background_color = btn_color,
                text = '"{}" by {} ({}) {}'.format(song.title, song.artist, song.year, learn_state))
            self.song_id_list.append(temp_button)
            self.root.ids.song_count.add_widget(temp_button)
            temp_button.bind(on_release = self.handle_mark)
        self.song_status()

    def handle_mark(self, instance):
        btn = instance.id
        for song in self.songs.songs:
            validate = '{}_{}'.format(song.title, song.year)
            if btn == validate:
                if song.is_learned == True:
                    self.root.ids.message_box.text = 'You have already learned {} ({})'.format(song.title, song.year)
                else:
                    self.songs.mark_as_learned(btn)
                    self.root.ids.message_box.text = ('You learned {} ({})'.format(song.title, song.year))
        give_list = self.songs.give_songs()
        self.make_entries(give_list)

    def exit_app(self):
        self.songs.save_songs()

    def clear_widget(self):
        for song_id in self.song_id_list:
            self.root.ids.song_count.remove_widget(song_id)

    def error_check(self):
        title_check = self.root.ids.input_title.text
        artist_check = self.root.ids.input_artist.text
        year_check = self.root.ids.input_year.text
        error_state = ''
        if title_check == '' or artist_check == '' or year_check == '':
            error_state = 'Blank'
        else:
            try:
                int(year_check)
            except ValueError:
                error_state = 'Type'
            else:
                if int(year_check) > 2020 or int(year_check) < 1800:
                    error_state = 'Invalid'
        for song in self.songs.songs:
            if title_check == song.title and artist_check == song.artist and year_check == song.year:
                error_state = 'Duplicate'
        return error_state

    def handle_stop(self):
        self.songs.save_songs()
        sys.exit(0)



if __name__ == '__main__':
    SongsToLearnApp().run()
