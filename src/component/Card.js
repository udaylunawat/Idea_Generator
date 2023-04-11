import React from 'react'
import { Card as Cards, Col, Row } from 'antd';
import classes from './Card.module.css'

const Card = (props) => {
    let data = props.data;

    // Convert string keys with string values to an array of objects
    if (typeof data === 'object' && !Array.isArray(data)) {
        data = Object.keys(data).map((key) => {
            return { name: key, content: data[key] };
        });
    }

    return (
        <>
            <Row gutter={16}>
                {data.map((item, index) => {
                    return (
                        <Col span={8} key={index}>
                            <Cards className={classes.testing} title={item.name} bordered={true}>
                                <i>{item.content}</i>
                            </Cards>
                        </Col>
                    )
                })}
            </Row>
        </>
    )
}

export default Card



// import React from 'react'
// import { Card as Cards, Col, Row } from 'antd';
// import classes from './Card.module.css'

// const Card = (props) => {
//     let data = props.data;

//     // Convert object to array if necessary
//     if (typeof data === 'object' && !Array.isArray(data)) {
//         data = Object.keys(data).map((key) => {
//             return { name: key, content: data[key] };
//         });
//     }

//     return (
//         <>
//             <Row gutter={16}>
//                 {data.map((item, index) => {
//                     return (
//                         <Col span={8}>
//                             <Cards className={classes.testing} title={item.name} bordered={true}>
//                                 <i>{item.content}</i>
//                             </Cards>
//                         </Col>
//                     )
//                 })}
//             </Row>
//         </>
//     )
// }

// export default Card