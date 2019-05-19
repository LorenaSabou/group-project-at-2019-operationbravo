import React from 'react';
import axios from 'axios';
import ReactTable from "react-table";
import "react-table/react-table.css";

class PageContent extends React.Component{


    constructor(props){
        super(props);
        this.state = {
            rooms : [
            ]
        };
        this.recheck = this.recheck.bind(this);
    }

    componentDidMount() {
        axios.get('http://localhost:1331/predict')
            .then(res => {
                this.setState({rooms: res.data['rooms']});
        });
    }

    findPositionById(roomId) {
        return this.state.rooms.findIndex(x => x.roomId == roomId);
    }

    recheck(roomId){
        const pos = this.findPositionById(roomId);
        axios.get('http://localhost:1331/predict_room/' + roomId).then(room => {
            this.setState(oldState => {
                let rooms = oldState.rooms.slice();
                let copy = Object.assign({}, rooms[pos]);
                copy.num_persons = room.num_persons;
                rooms[pos] = copy;
                return {
                    rooms: rooms
                };
            });
        });
    }

    render(){

        const columns = [
            {
                Header: "Room Id",
                accessor: "id",
                style: {
                    textAlign: "center"
                }
            },
            {
                Header: "Room Name",
                accessor: "room_name",
                style: {
                    textAlign: "center"
                }
            },
            {
                Header: "Number of Persons",
                accessor: "num_persons",
                style: {
                    textAlign: "center"
                }
            },
            {
                Header: "Action",
                Cell: props =>{
                    return (<button type="button"
                                    onClick={() => {
                                           this.recheck(props.original.id)
                                        }}>Recheck</button>)
                },
                style: {
                    textAlign: "center"
                }

            },
        ];

        const data = this.state.rooms;
        return <div>
            <ReactTable
                columns = {columns}
                data={data}
                showPagination={false}
                defaultPageSize={this.state.rooms.length}>
            </ReactTable>
        </div>
    }
}


export default PageContent;
