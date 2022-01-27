"""codeauthor:: Brand Hauser"""
from communication.input_listener import InputListener
from data.values import Status
from multiprocessing import Queue
from motion_sensing.motion_sensor import MotionSensor

status = Status.READY


def build_target_colors():
    """Build a list of color values for each team in the game.
    :returns: list of team_color objects"""
    colors_list = []
    return colors_list


def run():
    """Runs the algorithm of the overall control.  Listens for messages from
    IR sensors as well as hits and responds accordingly."""
    while True:
        pass


if __name__ == '__main__':
    # command_queue = ()
    motion_queue = Queue(1)
    # colors = build_target_colors()
    # messenger = Messenger()
    # targeter = Targeter(command_queue, motion_queue, colors, messenger)
    # targeter.daemon = True
    # targeter.start()
    # play_start_sound()

    # Create motion detector object
    motion_detector = MotionSensor(motion_queue)

    # Create IR listener
    motionListener = InputListener(motion_detector)

    # Start required threads
    motionListener.start()
    motion_detector.start()
    run()
