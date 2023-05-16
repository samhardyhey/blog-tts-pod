import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)


def to_snake_case(s):
    """
    Converts a string to snake case.
    """
    # Replace spaces and dashes with underscores
    s = s.replace(" ", "_")
    s = s.replace("-", "_")

    # Split the string into words
    words = s.split()

    return "_".join(word.lower() for word in words)


nautilus_editors_note = """'Behold the humble nautilus. Just about a foot in diameter, it is a slow bottom-dweller with short tentacles that moves through the water with an unsteady wobble. It\'s also 500 million years old and, in its day, was the best and brightest, using its newly evolved depth control to lay waste to acre after acre of scuttling crustacean prey.\',\n \'We became interested in it here at Nautilus because, well, we stole its name. But also because (for a mollusk) it represents a remarkable intersection of science, math, myth, and culture. Since that is exactly the kind of intersection we love to write about, we decided to put together a little "teaser" issue all about it.\',\n \'There\'s the science. The nautilus has a beautiful, logarithmic, and fractal spiral in its shell. Benoit Mandelbrot, discoverer of the fractal, gives us a few words on that topic. One of the world\'s foremost nautilus experts, Peter Ward, tells us about nautilus evolution and biology, and about his life of nautilus research.\',\n \'Then, the myth: from Jules Verne\'s fictional submarine, to Oliver Wendell Holmes\' poem, to how and why we turn science into story.\',\n \'Two chapters, one undersea creature. Welcome aboard.'"""
