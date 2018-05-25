import tweepy

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main():
  # Fill in the values noted in previous step here
  cfg = {
    "consumer_key"        : "zMGtWnPaGxT9yVWJmmt8GTgB7",
    "consumer_secret"     : "t95ytV7GmfD24RrHo8mwYOqjzRINAPhXJgq9YsnINmxl7tRknx",
    "access_token"        : "367687030-L1hyWuQDGe01zfW6ZdxWq8qj5lNLr29kiigVwrVs",
    "access_token_secret" : "1fcK0kzfkysHOEHF57PSxQfqMMjjGMkHoxwSJYPrtiZJU"
    }

  api = get_api(cfg)
  tweet = "Marco e' un coglione!"
  status = api.update_status(status=tweet)
  # Yes, tweet is called 'status' rather confusing

if __name__ == "__main__":
  main()
