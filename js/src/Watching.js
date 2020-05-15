import React from 'react'

import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Typography from '@material-ui/core/Typography'

import WatchingIcon from 'mdi-react/EyeOutlineIcon'

import CardIconHeader from './util/CardIconHeader'


const Watching = () => {
  return (
    <Card>
      <CardIconHeader
        icon={<WatchingIcon />}
        title='How to Watch Recorded Games'
      />
      <CardContent>
        <Typography>Download a match you want to watch and extract the zip. The following sections represent common configurations. Pick the one that matches the type of recorded game you downloaded and your system setup.</Typography>
        <br />
        <Typography variant='h6'>Definitive Edition</Typography>
        <Typography>
          <ol>
            <li>Open Age of Empires II: Definitive Edition</li>
            <li>Select "Saves & Replays" from the main menu</li>
            <li>Select "Open Saved Games Folder" from the bottom row of buttons</li>
            <li>Move the extracted recorded game to the folder that opens</li>
            <li>Select "Return to Main Menu" from the bottom row of buttons</li>
            <li>Select "Saves & Replays" from the main menu again</li>
            <li>Select the tab labeled "Replays"</li>
            <li>Select the match from the list and select "Load Game"</li>
          </ol>
          <Typography>Note: You can skip steps 3-6 if you create a shortcut to the Saved Games folder or otherwise save the path. Furthermore, remember that only recorded games from the latest patch can be watched on Definitive Edition.</Typography>
          <br />
        </Typography>
        <Typography variant='h6'>Wololo Kingdoms + Userpatch 1.5 + Voobly</Typography>
        <Typography>
          <ol>
            <li>Navigate to your Age of Empires II install location. It's normally at <code>C:\Program Files (x86)\Microsoft Games\Age of Empires II</code></li>
            <li>Navigate to the <code>Voobly Mods\AOC\Data Mods\WololoKingdoms\SaveGame</code> folder</li>
            <li>Move the extracted recorded game to the <code>SaveGame</code> folder</li>
            <li>Open a lobby on Voobly</li>
            <li>Select "Settings" in the lobby</li>
            <li>Ensure patch "v1.5 RC" is selected</li>
            <li>Check "Mod" and select "WololoKingdoms"</li>
            <li>Select "Watch Recording" from the left menu</li>
            <li>Check "Load a game recording"</li>
            <li>Select the match from the list</li>
            <li>Select "OK" to close the settings</li>
            <li>Select "Launch"</li>
          </ol>
        </Typography>
        <Typography variant='h6'>The Conquerors 1.0c</Typography>
        <Typography>
          <ol>
            <li>Navigate to your Age of Empires II install location. It's normally at <code>C:\Program Files (x86)\Microsoft Games\Age of Empires II</code></li>
            <li>Navigate to the <code>SaveGame</code> folder</li>
            <li>Move the extracted recorded game to the <code>SaveGame</code> folder</li>
            <li>Launch Age of Empires II</li>
            <li>Select "Single Player"</li>
            <li>Select "Saved and Recorded Games"</li>
            <li>Select the match from the list</li>
            <li>Select "Ok"</li>
          </ol>
        </Typography>
        <Typography variant='h6'>Other</Typography>
        <Typography>If the recorded game does not match one of the configurations listed, try these tips.</Typography>
        <Typography>
          <ol>
            <li>If it's a Userpatch match, you can use the "Patch" selection on Voobly to pick the correct patch or the version switcher Voobly provides when manually launching <code>age2_x1.exe</code></li>
            <li>If it's pre-1.0c, use a version switcher to jump back to an earlier version</li>
          </ol>
        </Typography>
      </CardContent>
    </Card>
  )
}

export default Watching
