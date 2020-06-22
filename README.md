# aocrecs.com

Code for the website [aocrecs.com](https://aocrecs.com). Includes both the server component and website interface.

## Setup

Define the following environmental variables:

Variable | Purpose | Example
--- | --- | ---
`MGZ_DB` | URL to MGZ database. | `postgresql://username:password@localhost:5432/mgzdb`
`MGZ_GTM` | Google Tag Manager ID. | `UA-10051774-7`
`AWS_ACCESS_KEY_ID` | AWS access key ID. |
`AWS_SECRET_ACCESS_KEY` | AWS secret access key. |
`VOOBLY_USERNAME` | Voobly username (to access metadata while uploading). |
`VOOBLY_PASSWORD` | Voobly password. |

The AWS keys provide access to the S3 bucket storing the compressed recorded games. The Voobly credentials are used to fetch account metadata when adding uploaded matches.

SSL certificate data must exist at `data/`. Follow the guide [here](https://medium.com/@pentacent/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71). `docker-compose.yaml` is pre-configured.

`docker-compose build` will build all required images.

## Deploy

`docker-compose up -d` will launch three containers:
  - Python server
  - nginx (reverse proxy in front of server; host for static Javascript assets)
  - certbot (for SSL certificate renewal)

## Development

### Server (`python/`)

Create a Python virtual environment (Python 3.6+) and enter it: `python3 -m venv venv && venv/bin/activate`

Install dependencies: `pip install -e .`

Launch the Python server:

`uvicorn aocrecs.main:APP` (specify `--host` and `--port` as necessary)

### UI (`js/`)

Ensure that `node` and `yarn` are installed.

Install dependencies: `yarn`

Launch the `create-react-app` development server (from `js/`):

`REACT_APP_API="http://<server_host>:<server_port>/api" REACT_APP_GTM="<gtm_id>" yarn start` (set `HOSTNAME` and `PORT` as necessary)

## Contributions

Pull requests are welcome. If you want to add a feature that requires access to the data, contact me on Discord (`happyleaves#4133`) to arrange read-only database access.


## License

aocrecs.com / aoe2recs.com

Copyright © 2019-2020 happyleaves

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.
