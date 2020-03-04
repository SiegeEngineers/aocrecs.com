import React from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Link from '@material-ui/core/Link'
import Typography from '@material-ui/core/Typography'

import AboutIcon from 'mdi-react/InformationIcon'

import CardIconHeader from './util/CardIconHeader'


const About = () => {
  return (
    <Card>
      <CardIconHeader
        icon={<AboutIcon />}
        title='About'
      />
      <CardContent>
        <Typography variant='h6'>Contact</Typography>
        <Typography>
          <ul>
            <li>A project of <Link target="_blank" href="https://github.com/SiegeEngineers">Siege Engineers</Link></li>
            <li>Visit us on <Link target="_blank" href="https://discordapp.com/invite/njAsNuD">Discord</Link></li>
            <li>Point of contact: <Link href="mailto:happyleaves.tfr@gmail.com">HappyLeaves</Link></li>
          </ul>
        </Typography>
        <Typography variant='h6'>Open Source</Typography>
        <Typography>
          <ul>
            <li><Link href="https://github.com/siegeengineers/aocrecs.com">Website</Link></li>
            <li><Link href="https://github.com/siegeengineers/aoc-mgz-db">Database</Link></li>
            <li><Link href="https://github.com/happyleavesaoc/aoc-mgz">Parser</Link></li>
          </ul>
        </Typography>
      </CardContent>
    </Card>
  )
}

export default About
