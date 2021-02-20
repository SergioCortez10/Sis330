import os 
import glob
import panda as pd 
import xml.etree.ElementTree as ET

def xlm_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/".xml"'):
        tree =ET.parse(xml_file)
        root = tree.getroot()

        for member in root.findall('object'):
            value = ('data/'+root.find('filename').text,
                    int(member[4][0].text),
                    int(member[4][1].text),
                    int(member[4][2].text),
                    int(member[4][3].text),
                    member[0].text,
                    )
            xml_list.append(value)
    column_name = ['filename','xmin','ymin','xmax','ymax','class']
    xml_df = pd.DataFrame(xml_list,column = column_name)
    return xml_df

image_path = os.path.join(os.getcwd(), 'dataset2/with_mask/')
dataset_df = xlm_to_csv(image_path)

print('completado')