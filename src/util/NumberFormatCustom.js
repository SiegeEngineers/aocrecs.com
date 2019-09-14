import React from 'react'
import NumberFormat from 'react-number-format'

const NumberFormatCustom = ({inputRef, onChange, ...other}) => {
  return (
    <NumberFormat
      {...other}
      getInputRef={inputRef}
      onValueChange={values => {
        onChange({
          target: {
            value: values.value,
          },
        })
      }}
    />
  )
}

export default NumberFormatCustom
