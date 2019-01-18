import React from "react"

export default function (props) {
    return (
        <select
            className={props.className || "form-control"}
            disabled={props.disabled || false}
            id={props.id || null}
            onChange={props.onChange}
            value={props.value}
        >
            {props.choices.map((item) => {
                return (
                    <option
                        key={item}
                        value={item}>
                        {item}
                    </option>
                )
            })}
        </select>
    )
}