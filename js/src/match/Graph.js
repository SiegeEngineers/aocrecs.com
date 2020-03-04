import React from 'react'
import {useTheme} from '@material-ui/styles'
import Typography from '@material-ui/core/Typography'

import {ForceGraph3D} from 'react-force-graph'
import SpriteText from 'three-spritetext'

import {PLAYER_COLORS} from '../util/Shared'
import DataQuery from '../util/DataQuery'
import Help from '../util/Help'
import GetGraph from '../graphql/Graph'


const Graph = ({match}) => {
  const theme = useTheme()
  return (
    <>
    <Typography variant='h6'>Kill Graph <Help text='Graph of all kills by military units. Arrows go from the killer to the victim. Units are labeled as their type at creation.' /></Typography>
    <DataQuery query={GetGraph} variables={{match_id: match.id}}>
      {(data) => (
        <ForceGraph3D
          backgroundColor={theme.palette.grey['800']}
          width={800}
          height={800}
          graphData={data.match.graph}
          showNavInfo={false}
          linkWidth={1}
          linkOpacity={1}
          linkDirectionalArrowLength={10}
          linkDirectionalArrowRelPos={1}
          enablePointerInteraction={false}
          linkDirectionalArrowResolution={3}
          linkResolution={3}
          nodeThreeObject={node => {
            const sprite = new SpriteText(node.name)
            sprite.color = PLAYER_COLORS[node.color_id + 1]
            sprite.textHeight = 8
            sprite.fontWeight = 'bold'
           return sprite;
         }}
        />
      )}
    </DataQuery>
    </>
  )
}

export default Graph
