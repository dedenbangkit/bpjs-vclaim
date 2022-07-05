# VCLAIM BPJS

I made this for my in-laws, he need an easy access for his personal development needs, but written in C++ (OMG). Since there is no clear documentation from him about this BPJS VClaim, I looked for anything related to this service modules on github. Then I found [morizbebenk/flask-bpjs](https://github.com/morizbebenk/flask-bpjs), a webservice used to handle the decryption process of data response from bridging BPJS VClaim v2.0 (Encrypted Version). This is the simple CLI version of it! most of the lines are removed. Plus, the Docker version!

## Environment Setup

```bash
$ export VCLAIM_ID="VCLAIM_ID"
$ export SECRET_ID="SECRET_ID"
$ export USER_KEY="USER_KEY"
$ export SERVICE_URL="https://apijkn.bpjs-kesehatan.go.id"
$ export REST_URL="vclaim-rest"
```

## Installation and Usage

### Python Venv

Install Requirements

```bash
$ python -m venv virtualenv
$ source virtualenv/bin/activate
$ pip install -r requirements
```

Example:

```
$ python bpjs.py referensi/kelasrawat | jq
{
  "list": [
    {
      "kode": "1",
      "nama": "VVIP"
    },
    {
      "kode": "2",
      "nama": "VIP"
    },
    {
      "kode": "3",
      "nama": "Kelas 1"
    },
    {
      "kode": "4",
      "nama": "Kelas 2"
    },
    {
      "kode": "5",
      "nama": "Kelas 3"
    }
  ]
}
```

### Docker

Build:

```bash
$ docker build -t bpjs/vclaim .
```

Example:

```bash
$ docker run \
        --env VCLAIM_ID="${VCLAIM_ID}" \
        --env SECRET_ID="${SECRET_ID}" \
        --env USER_KEY="${USER_KEY}" \
        --env SERVICE_URL="${SERVICE_URL}" \
        --env REST_URL="${REST_URL}" \
        bpjs/vclaim referensi/kelasrawat \
        | jq -r '.list \
            | ["kode","nama"], ["--","------"], (.[] \
            | [.kode, .nama]) \
            | @tsv'
kode    nama
--      ------
1       VVIP
2       VIP
3       Kelas 1
4       Kelas 2
5       Kelas 3

```


## See also:
- Endpoints collections (Written in PHP): [aamdsam/bridging-bpjs](https://github.com/aamdsam/bridging-bpjs/tree/dev/src/VClaim)
