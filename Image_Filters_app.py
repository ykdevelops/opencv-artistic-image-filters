import io
import base64
import cv2
from PIL import Image
from filters import *

# Generating a link to download a particular image file.
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format = 'JPEG')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Set title.
st.title('Artistic Image Filters')

# Upload image.
uploaded_file = st.file_uploader('Choose an image file:', type=['png','jpg'])

if uploaded_file is not None:
    # Convert the file to an opencv image.
    raw_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
    input_col, output_col = st.columns(2)
    with input_col:
        st.header('Original')
        # Display uploaded image.
        st.image(img, channels='BGR', use_column_width=True)

    st.header('Filter Examples:')
    # Display a selection box for choosing the filter to apply.
    option = st.selectbox('Select a filter:',
                          ( 'None',
                            'Color Dodge',
                            'Emboss',
                            'Water Color',
                            'Cartoon',
                         ))

    # Define columns for thumbnail images.
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.caption('Color Dodge')
        st.image('color_dodge.png')
    with col2:
        st.caption('Emboss')
        st.image('emboss.png')
    with col3:
        st.caption('Water Color')
        st.image('watercolor.png')
    with col4:
        st.caption('Cartoon')
        st.image('cartoon.png')

    # Flag for showing output image.
    output_flag = 1
    # Colorspace of output image.
    color = 'BGR'

     # Generate filtered image based on the selected option.
    if option == 'None':
        # Don't show output image.
        output_flag = 0
    elif option == 'Color Dodge':
        output = color_dodge(img)
        color = 'GRAY'
    elif option == 'Emboss':
        output = emboss(img, 3)
        color = 'GRAY'
    elif option == 'Water Color':
        level = st.slider('level', 0, 5, 2)
        output = watercolor(img, level)
    elif option == 'Cartoon':
        output = cartoon(img)
        color = 'GRAY'

    with output_col:
        if output_flag == 1:
            st.header('Output')
            st.image(output, channels=color)
            # fromarray convert cv2 image into PIL format for saving it using download link.
            if color == 'BGR':
                result = Image.fromarray(output[:,:,::-1])
            else:
                result = Image.fromarray(output)
            # Display link.
            st.markdown(get_image_download_link(result,'output.png','Download '+'Output'),
                        unsafe_allow_html=True)
    