from kivy.clock import Clock

def my_callback(dt):
    print('My callback is called !')

Clock.schedule_interval(my_callback, 1)
