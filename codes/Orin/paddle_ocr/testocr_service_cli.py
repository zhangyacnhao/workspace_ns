import requests
import base64

def read_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_ocr_service(image_base64, url):
    response = requests.post(
        url,
        data={'image': image_base64},
    )
    return response.json()

def main():
    image_path = 'screenshot.png'
    image_base64 = read_image_as_base64(image_path)

    urls = {
        'predict_ocr': 'http://0.0.0.0:8001/predict_ocr',
    }

    predict_ocr_response = test_ocr_service(image_base64, urls['predict_ocr'])
    print("predict_ocr response:", predict_ocr_response)


if __name__ == "__main__":
    main()

