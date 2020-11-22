from concurrent.futures import ThreadPoolExecutor
import boto3
import json

class Lambda:
    def __init__(self):
        self.results = []
        self.s3 = boto3.client(
            'lambda',
            region_name='us-east-2',
            aws_access_key_id='AKIAIFKMXDBM5VEGPEJQ',
            aws_secret_access_key='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'
        );

    def request_image(self, image):
        print("making request", image);

        payload = json.dumps({
            "image": image    
        });
        response = self.s3.invoke(
            FunctionName='arn:aws:lambda:us-east-2:579551894421:function:CaptionImage',
            InvocationType='RequestResponse',
            Payload=payload
        );
        json_response = json.loads(response['Payload'].read())
        print("response comlete", image);
        return json_response

    def request(self, images):
        with ThreadPoolExecutor(max_workers=100) as executor:
            futs = []
            for image in images:
                futs.append(
                    executor.submit(
                        self.request_image,
                        image = image
                    )
                )

            self.results = []
            for fut in futs:
                self.results.append(fut.result())
        return self.results


print(Lambda().request([1,2,3,4,5,6,7,8]))