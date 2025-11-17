import boto3, requests

s3 = boto3.client('s3', region_name="us-east-1")
bucket = 'ds2002-f25-kgy4dc'
object_name = 'omg.gif'
expires_in = 60



url = "https://media.tenor.com/rLjeBvC0v94AAAAM/oh-my.gif"
save_path = "omg.gif"

response = requests.get(url)



with open(save_path, "wb") as f:
    f.write(response.content)

s3.upload_file(save_path, bucket, object_name)

url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': object_name},
    ExpiresIn = expires_in
)

print("\nPresigned URL:")
print(url)