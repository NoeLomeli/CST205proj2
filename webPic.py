import numpy as np
import cv2
from PIL import Image, ImageDraw

def facechop():
    facedata = "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(facedata)


    source_image = Image.open('test_image.jpg')
    source_width, source_height = source_image.size
    print 'Image is {}x{}'.format(source_width, source_height)

    target_width = 320
    target_height = 243

    # Make image a reasonable size to work with. Using the source_height will
    # make sure it's just resized to the target_width
    source_image.thumbnail((target_width, source_height), Image.ANTIALIAS)
    # Find the faces and show us where they are
    def faces_from_pil_image(pil_image):
        "Return a list of (x,y,h,w) tuples for faces detected in the PIL image"
        storage = cv2.FileStorage()
        #facial_features = cv2.Load('haarcascade_frontalface_alt.xml')
        #cv_im = cv2.CreateImageHeader(pil_image.size, cv2.IPL_DEPTH_8U, 3)
        #cv2.SetData(cv_im, pil_image.tostring())
        #faces = cv2.HaarDetectObjects(cv_im, facial_features, storage)
        # faces includes a `neighbors` field that we aren't going to use here
        return [f[0] for f in faces]

    faces = faces_from_pil_image(source_image)
    faces_found_image = draw_faces(source_image, faces)
    faces_found_image.show()

    # Get details about where the faces are so we can crop
    top_of_faces = top_face_top(faces)
    bottom_of_faces = bottom_face_bottom(faces)

    all_faces_height = bottom_of_faces - top_of_faces
    print 'Faces are {} pixels high'.format(all_faces_height)

    if all_faces_height >= target_width:
        print 'Faces take up more than the final image, you need better logic'
        exit_code = 1
    else:
        # Figure out where to crop and show the results
        face_buffer = 0.5 * (target_height - all_faces_height)
        top_of_crop = int(top_of_faces - face_buffer)
        coords = (0, top_of_crop, target_width, top_of_crop + target_height)
        print 'Cropping to', coords
        final_image = source_image.crop(coords)
        final_image.show()
        exit_code = 0

    return exit_code



    def draw_faces(image_, faces):
        "Draw a rectangle around each face discovered"
        image = image_.copy()
        drawable = ImageDraw.Draw(image)

        for x, y, w, h in faces:
            absolute_coords = (x, y, x + w, y + h)

            drawable.rectangle(absolute_coords)
        return image

    def top_face_top(faces):
        coords = [f[1] for f in faces]
        # Top left corner is 0,0 so we need the min for highest face
        return min(coords)


    def bottom_face_bottom(faces):
        # Top left corner is 0,0 so we need the max for lowest face. Also add the
        # height of the faces so that we get the bottom of it
        coords = [f[1] + f[3] for f in faces]
        return max(coords)

    #minisize = (img.shape[1],img.shape[0])
    #miniframe = cv2.resize(img, minisize)
    '''
    faces = cascade.detectMultiScale(miniframe)

    for f in faces:
        x, y, w, h = [ v for v in f ]
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))

        sub_face = img[y:y+h, x:x+w]
        face_file_name = "faces/face_" + str(y) + ".jpg"
        cv2.imwrite(face_file_name, sub_face)
'''
    cv2.imshow(image, img)

    return

if __name__ == '__main__':
    facechop()

    while(True):
        key = cv2.waitKey(20)
        if key in [27, ord('Q'), ord('q')]:
            break
