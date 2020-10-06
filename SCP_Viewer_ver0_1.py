from Viewer_gui_control import viewer_gui_control

gui_h = viewer_gui_control()
gui_h.daemon = True
gui_h.start()

