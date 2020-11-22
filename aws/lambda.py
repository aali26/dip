from concurrent.futures import ThreadPoolExecutor
import boto3
import json

class Lambda:
    def __init__(self):
        self.results = []
        self.s3 = boto3.client(
            'lambda',
            region_name='us-east-2',
            aws_access_key_id='AKIAXZY6WBOZGF2GO6MD',
            aws_secret_access_key='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'
        );

    def request_image(self, image):
        print("making request", image);

        payload = json.dumps({
            image: image    
        });
        response = self.s3.invoke(
            FunctionName='arn:aws:lambda:us-east-2:536398400434:function:Caption',
            InvocationType='RequestResponse',
            Payload=payload
        );
        json_response = json.loads(response['Payload'].read())
        print("response comlete", image);
        return json_response

    def request(self, images):
        with ThreadPoolExecutor(max_workers=5) as executor:
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