"""
Audio Project - Virtual Piano Program
Stephanie Chan
09/14/12
Dependencies:
Python 2.7
NumPy, SciPy, PyGame, Scikits.samplerate
"""

import numpy, pygame, sys,os
#from scikits.samplerate import resample
from pygame.locals import *

def generate_scale():
    """
    Given the initial note, middle C, create the rest of the musical scale by
    resampling.
    
    Returns: Dictionary of musical scale with the key being the name of the note
    and the value being the corresponding sound object.
    
    """    
    pygame.mixer.init()
    
    wav = "piano-c.wav"
    sound = pygame.mixer.Sound(wav)
    sndarray = pygame.sndarray.array(sound)

    ratio_dict = {'low_c': 1, 'c_sharp': .944, 'd': .891, 'd_sharp':.841, 'e':.794,
                  'f':.749, 'f_sharp': .707, 'g': .667, 'g_sharp': .63, 'a': .594,
                  'a_sharp': .561, 'b':.53, 'high_c':.5}
    
    # Generate the Sound objects from the dictionary.
    scale_dict = {}
    #for key,value in ratio_dict.iteritems():
        #smp = resample(sndarray, value,"sinc_fastest").astype(sndarray.dtype)
        # Use the key, currently a string, as a variable
        #scale_dict[key] = pygame.sndarray.make_sound(smp)
    return scale_dict

def load_image(name):
    """
    Loads image into pygame and converts into a faster to render object
    """
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()
        
class Keyboard(pygame.sprite.Sprite):
    """
    A keyboard sprite class for generating all the key images and making it
    light up on key press.
    
    """
    def __init__(self,note,x,y, sharp=False):
        """
        Input:
        :note: string name of the instance's note
        :x: :y: position values for rect area
        :sharp: boolean for differentiating between white and black keys
        """
        self.clock = pygame.time.Clock()
        pygame.sprite.Sprite.__init__(self)
        self.note = note
        self.sharp = sharp
        self.x = x
        self.y = y
        if sharp:
            self.image, self.rect = load_image('black-key.png')
        else:
            self.image, self.rect = load_image('key-left.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = x, y

    def pressed(self):
        if self.sharp:
            self.image, self.rect = load_image('black-p-key.png')            
        else:
            self.image, self.rect = load_image('pressed-key.png')
        self.rect.topleft = self.x, self.y
        # wait one second before performing unhighlighting the key
        self.clock.set_timer(1, 1000)

    def unpressed(self):
        if self.sharp:
            self.image, self.rect = load_image('black-key.png')
        else:
            self.image, self.rect = load_image('key-left.png')
        self.rect.topleft = self.x, self.y

        
def main():
    pygame.init()

    # Load sound objects that will be used for key press
    scale_dict = generate_scale()

    # Window initialization
    screen=pygame.display.set_mode((800,600))
    pygame.display.set_caption("Virtual Piano")

    # Background text layer initialization
    background = pygame.Surface(screen.get_size())
    background = background.convert()

    # Text information to go o background
    if pygame.font:
        font = pygame.font.Font(None, 36)
        title = font.render("Virtual Piano", 1, (255, 255, 255))
        instructions = font.render("Each note corresponds to the following computer keys:", 1, (255,255,255))
        note = font.render("Note: C  C# D  D# E  F  F# G  G# A  A# B  C(high)", 1, (255,255,255))
        key =  font.render("Key:   A  W  S  E   D  F  R   H   Y   J  U   K   L", 1, (255,255,255))
        textpos = title.get_rect(top=410, left=10)
        instpos = instructions.get_rect(top=440, left=10)
        notepos = note.get_rect(top=470, left=10)
        keypos = key.get_rect(top=500, left=10)
        background.blit(title, textpos)
        background.blit(instructions, instpos)
        background.blit(note, notepos)
        background.blit(key, keypos)

    # Add background to screen. Added to hear to load before images.
    screen.blit(background, (0,0))
    pygame.display.flip()
    screen = pygame.display.get_surface()

    
    note_str = ['low_c', 'c_sharp', 'd', 'd_sharp', 'e','f', 'f_sharp', 'g',
                 'g_sharp', 'a', 'a_sharp', 'b', 'high_c']
    sprites = {}
    # layers will be used to differentiate black key and white key layers
    layers = pygame.sprite.LayeredUpdates()
    x = 0 
    y = 0

    # Generate keyboard objects that goes into the sprite dictionary with the
    # key being the string name and the value being the keyboard instance
    for note in note_str:
        z = 0 
        if note.endswith('sharp'):
            z = x - 31
            sprites[note] = Keyboard(note,z,y, sharp=True)
            layers.add(sprites[note])
            layers.change_layer(sprites[note],1)
        else:
            sprites[note] = Keyboard(note,x,y)
            layers.add(sprites[note])
            x+=101

    # Sprites will be ordered by layer which is exactly how we want to render it
    allsprites = pygame.sprite.OrderedUpdates(tuple(layers.sprites()))
    pygame.display.update()
    
    def input(events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            # Event called immediately after a keyboard press event after a time delay
            if event.type == 1:
                for i in sprites.keys():
                    sprites[i].unpressed()
            if event.type == KEYDOWN:
                if event.key == ord('a'):
                    scale_dict['low_c'].play()
                    sprites['low_c'].pressed()
                if event.key == ord('w'):
                    scale_dict['c_sharp'].play()
                    sprites['c_sharp'].pressed()
                if event.key == ord('s'):
                    scale_dict['d'].play()
                    sprites['d'].pressed()
                if event.key == ord('e'): 
                    scale_dict['d_sharp'].play() 
                    sprites['d_sharp'].pressed()
                if event.key == ord('d'):
                    scale_dict['e'].play()
                    sprites['e'].pressed()
                if event.key == ord('f'):
                    scale_dict['f'].play()
                    sprites['f'].pressed()
                if event.key == ord('r'):
                    scale_dict['f_sharp'].play()
                    sprites['f_sharp'].pressed()
                if event.key == ord('h'):
                    scale_dict['g'].play()
                    sprites['g'].pressed()
                if event.key == ord('y'):
                    scale_dict['g_sharp'].play()
                    sprites['g_sharp'].pressed()
                if event.key == ord('j'):
                    scale_dict['a'].play()
                    sprites['a'].pressed()
                if event.key == ord('u'):
                    scale_dict['a_sharp'].play()
                    sprites['a_sharp'].pressed()
                if event.key == ord('k'):
                    scale_dict['b'].play()
                    sprites['b'].pressed()
                if event.key == ord('l'):
                    scale_dict['high_c'].play()
                    sprites['high_c'].pressed()

    while True:
        input(pygame.event.get())
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
