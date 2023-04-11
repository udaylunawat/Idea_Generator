import React from 'react'
import { Button, Input as Inputs, Space,Card } from 'antd';
import classes from './Input.module.css'
const Input =({ onButtonClick, onInputChange, onDemoClick })=> {

  return (
    <>
      <div className={classes.inputContainer}>
        <Card className={classes.cardBackgroundColor}>
          <Space.Compact style={{ width: '100%' }}>
            <Inputs onChange={onInputChange} placeholder='please enter your queries' />
            <Button type="primary" onClick={onButtonClick}>Hit Me</Button>
            <Button type="primary" onClick={onDemoClick}>Demo</Button>
          </Space.Compact>
        </Card>
      </div>
    </>
  )
}

export default Input




// import React from 'react'
// import { Button, Input as Inputs, Space,Card } from 'antd';
// import classes from './Input.module.css'
// const Input =({ onButtonClick, onInputChange })=> {

//   return (
//     <>
//     <div className={classes.inputContainer}>
//         <Card className={classes.cardBackgroundColor}>
//       <Space.Compact style={{ width: '100%' }}>
//         <Inputs onChange={onInputChange} placeholder='please enter your queries' />
//         <Button type="primary" onClick={onButtonClick}>Hit Me</Button>
//       </Space.Compact>
//       </Card>
//     </div>
//     </>
//   )
// }

// export default Input
