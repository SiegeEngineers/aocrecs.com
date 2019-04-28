import React from 'react'
import WinnerIcon from 'mdi-react/TrophyVariantIcon'

const WinnerMark = ({winner, className}) => {
  return (
    <span>{winner
      ? <WinnerIcon className={className} />
      : <svg className={className} />
    }</span>
  )
}

export default WinnerMark
