import os
import numpy as np
import PIL.Image

directory = os.getcwd() + os.sep
output_directory = directory + 'picture' + os.sep

# list_im = [['fims11.png', 'ifms11.png', 'mfsi11.png', 'fmsi11.png'],
#            ['fsmi11.png', 'sfmi11.png', 'imsf1100.png', 'misf1100.png'],
#            ['ismf1100.png', 'simf1100.png', 'msfi1001.png', 'smfi1001.png']]
list_im = [['fims2520.png', 'ifms2520.png', 'mfsi2050.png', 'fmsi2050.png'],
           ['fsmi2550.png', 'sfmi2550.png', 'imsf202000.png', 'misf202000.png'],
           ['ismf252000.png', 'simf252000.png', 'msfi200050.png', 'smfi200050.png']]
# list_im = [['fims11.png', 'fims2520.png', 'ifms11.png', 'ifms2520.png'],
#            ['mfsi11.png', 'mfsi2050.png', 'fmsi11.png', 'fmsi2050.png'],
#            ['fsmi11.png', 'fsmi2550.png', 'sfmi11.png', 'sfmi2550.png']]
# list_im = [['imsf1100.png', 'imsf202000.png', 'misf1100.png', 'misf202000.png'],
#            ['ismf1100.png', 'ismf252000.png', 'simf1100.png', 'simf252000.png'],
#            ['msfi1001.png', 'msfi200050.png', 'smfi1001.png', 'smfi200050.png']]
horizened_im = []

for x in range(len(list_im)):
    imgs = [PIL.Image.open(output_directory + i) for i in list_im[x]]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

    # save that beautiful picture
    imgs_comb = PIL.Image.fromarray(imgs_comb)
    horizened_im.append('h' + str(x) + '.png')
    imgs_comb.save(output_directory + horizened_im[x])

# for a vertical stacking it is simple: use vstack
imgs = [PIL.Image.open(output_directory + i) for i in horizened_im]
min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
imgs_comb = PIL.Image.fromarray(imgs_comb)
imgs_comb.save(output_directory + 'Trifecta_vertical.jpg')
