import PySimpleGUI as sg
import os.path
import PIL.Image
import PIL.ImageOps
import PIL.ImageFilter
from PIL import ImageEnhance
import io
from pathlib import Path
import numpy as np

# Define the available filters and transformations
FILTERS = {
    "Escala de cinza": lambda img: img.convert("L").convert("RGB"),
    "Inversão de cores": lambda img: PIL.ImageOps.invert(img),
    "Aumento de contraste": lambda img: ImageEnhance.Contrast(img).enhance(1.5),
    "Desfoque": lambda img: img.filter(PIL.ImageFilter.BLUR),
    "Nitidez": lambda img: img.filter(PIL.ImageFilter.SHARPEN),
    "Detecção de bordas": lambda img: img.filter(PIL.ImageFilter.FIND_EDGES),
}

TRANSFORMATIONS = {
    "Rotacionar": lambda img, val: img.rotate(int(val))
}

def convert_to_bytes(img, resize=None):
    """Convert PIL image to bytes for PySimpleGUI to display"""
    if resize:
        img = img.resize(resize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

def apply_filters(image, selected_filters):
    """Apply multiple filters to an image"""
    result = image.copy()
    for filter_name in selected_filters:
        if filter_name in FILTERS:
            result = FILTERS[filter_name](result)
    return result

def apply_transformation(image, transform_type, value):
    """Apply transformation to an image"""
    if transform_type in TRANSFORMATIONS and value is not None:
        return TRANSFORMATIONS[transform_type](image, value)
    return image

def main():
    # Define the window layout
    sg.theme('DarkBlue3')
    
    # Create filter checkboxes
    filter_checkboxes = [[sg.Text('Filtros:')]]
    for filter_name in FILTERS.keys():
        filter_checkboxes.append([sg.Checkbox(filter_name, key=f'-FILTER-{filter_name}')])
    
    # Create transformation checkboxes with sliders
    transform_elements = [[sg.Text('Transformações:')]]
    transform_elements.append([sg.Checkbox('Rotacionar', key='-TRANSFORM-Rotacionar', enable_events=True)])
    transform_elements.append([sg.Text('Ângulo:', size=(6, 1)), 
                              sg.Slider(range=(-180, 180), default_value=0, size=(20, 15), 
                                        orientation='h', key='-SLIDER-Rotacionar', disabled=True)])
    left_col = [
        *filter_checkboxes,
        *transform_elements,
        [sg.Button('Aplicar', key='-APPLY-')],
        [sg.Button('Salvar Imagem', key='-SAVE-')],
        [sg.Button('Resetar', key='-RESET-')],
    ]
    
    right_col = [
        [sg.Text('Imagem Original')],
        [sg.Image(key='-ORIGINAL-')],
        [sg.Text('Imagem com Filtros')],
        [sg.Image(key='-MODIFIED-')]
    ]
    
    layout = [
        [sg.Text('Visualizador de Imagens com Filtros', font='Any 16')],
        [
            sg.Text('Selecionar Imagem: '),
            sg.Input(size=(25, 1), key='-FILENAME-', enable_events=True),
            sg.FileBrowse()
        ],
        [
            sg.Column(left_col, element_justification='c'),
            sg.VSeperator(),
            sg.Column(right_col, element_justification='c')
        ]
    ]

    window = sg.Window('Visualizador de Imagens', layout, resizable=True)

    original_img = None
    current_img = None
    last_selected_filters = []
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            break
            
        # Enable/disable sliders based on transformation checkboxes
        if event == '-TRANSFORM-Rotacionar':
            window['-SLIDER-Rotacionar'].update(disabled=not values['-TRANSFORM-Rotacionar'])

        # Automatically load image when file is selected
        if event == '-FILENAME-':
            filename = values['-FILENAME-']
            if os.path.exists(filename):
                try:
                    # Load the image and convert to RGB to ensure compatibility with all filters
                    original_img = PIL.Image.open(filename).convert('RGB')
                    current_img = original_img.copy()
                    
                    # Display the original image
                    img_width = min(400, original_img.width)
                    img_height = int(original_img.height * (img_width / original_img.width))
                    window['-ORIGINAL-'].update(data=convert_to_bytes(original_img, resize=(img_width, img_height)))
                    window['-MODIFIED-'].update(data=convert_to_bytes(original_img, resize=(img_width, img_height)))
                    
                    # Reset filters selection
                    for filter_name in FILTERS.keys():
                        window[f'-FILTER-{filter_name}'].update(False)
                    
                    # Reset transformation controls  
                    window['-TRANSFORM-Rotacionar'].update(False)
                    window['-SLIDER-Rotacionar'].update(value=0, disabled=True)

                    last_selected_filters = []
                except Exception as e:
                    sg.popup_error(f'Error loading image: {str(e)}')
            
        # Kept for compatibility
        if event == '-LOAD-':
            filename = values['-FILENAME-']
            if os.path.exists(filename):
                try:
                    # Load the image and convert to RGB to ensure compatibility with all filters
                    original_img = PIL.Image.open(filename).convert('RGB')
                    current_img = original_img.copy()
                    
                    # Display the original image
                    img_width = min(400, original_img.width)
                    img_height = int(original_img.height * (img_width / original_img.width))
                    window['-ORIGINAL-'].update(data=convert_to_bytes(original_img, resize=(img_width, img_height)))
                    window['-MODIFIED-'].update(data=convert_to_bytes(original_img, resize=(img_width, img_height)))
                    
                    # Reset filters selection
                    for filter_name in FILTERS.keys():
                        window[f'-FILTER-{filter_name}'].update(False)
                    
                    # Reset transformation controls  
                    window['-TRANSFORM-Rotacionar'].update(False)
                    window['-SLIDER-Rotacionar'].update(value=0, disabled=True)

                    last_selected_filters = []
                except Exception as e:
                    sg.popup_error(f'Error loading image: {str(e)}')
                    
        if event == '-APPLY-' and original_img is not None:
            # Get filters selected by checkboxes
            selected_filters = [filter_name for filter_name in FILTERS.keys() 
                               if values.get(f'-FILTER-{filter_name}', False)]
            
            try:
                # Apply the selected filters
                filtered_img = apply_filters(original_img, selected_filters)
                
                # Apply transformations based on checkboxes
                result_img = filtered_img.copy()
                
                # Apply rotation if selected
                if values['-TRANSFORM-Rotacionar']:
                    rotation_angle = int(values['-SLIDER-Rotacionar'])
                    result_img = TRANSFORMATIONS['Rotacionar'](result_img, rotation_angle)

                # Save the current state
                current_img = result_img
                last_selected_filters = selected_filters
                
                # Display the modified image
                img_width = min(400, result_img.width)
                img_height = int(result_img.height * (img_width / result_img.width))
                modified_image_bytes = convert_to_bytes(result_img, resize=(img_width, img_height))
                window['-MODIFIED-'].update(data=modified_image_bytes)
                print(f"Modified image updated: {len(modified_image_bytes)} bytes")
            except Exception as e:
                sg.popup_error(f'Error applying filters: {str(e)}')
        
        if event == '-RESET-' and original_img is not None:
            # Reset to the original image
            current_img = original_img.copy()
            
            # Clear all filter checkboxes
            for filter_name in FILTERS.keys():
                window[f'-FILTER-{filter_name}'].update(False)
                
            # Reset transformation controls
            window['-TRANSFORM-Rotacionar'].update(False)
            window['-SLIDER-Rotacionar'].update(value=0, disabled=True)

            last_selected_filters = []
            
            # Display the original image in both panels
            img_width = min(400, original_img.width)
            img_height = int(original_img.height * (img_width / original_img.width))
            window['-MODIFIED-'].update(data=convert_to_bytes(original_img, resize=(img_width, img_height)))
            
        if event == '-SAVE-' and current_img is not None:
            # Open a save file dialog
            save_filename = sg.popup_get_file('Save as', save_as=True, no_window=True)
            
            if save_filename:
                # Add file extension if not provided
                if not Path(save_filename).suffix:
                    save_filename += '.png'
                    
                try:
                    # Save the image
                    current_img.save(save_filename)
                    sg.popup(f'Image saved as {save_filename}')
                except Exception as e:
                    sg.popup_error(f'Error saving image: {str(e)}')

    window.close()

if __name__ == '__main__':
    main()