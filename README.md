# stitcher
code base to merge participant mind wandering reports with instructor screen captures

1. `slidegrabber.py` - takes in a video, and outputs cropped screenshotsof moments when slides changed. Outputs metadata for each video, a numpy array of percent change from moment-to-moment, and most importantly, a low-resolution still image for each relevant capture.
2. `MakePDF.ipynb` - Iterates through all of the captures, and assembles them into a PDF file (thus reconstituing the instructor's presentation), infers when a video is present and only saves the first and last capture from it (to avoid hundreds of captures). Outputs a PDF of the lecture, and a file containing the start and stopping indices of inferred video presentations.
3. `MW Classroom F2019.ipynb` - Generic preprocessing script for student attention data collected using our app. This will pool all of the student responses together and do some basic cleaning, plotting, and statistical analysis. Necessary for last step, wherein responses are stitched together with screengrabs.
4. `ClassPlot.ipynb` - Creates a visualization of the time course of the lecture, with plots showing the individual slides, where they fell on the timeline, and also the student responses for that lecture, and averaged responses across the entire duration of the study.
