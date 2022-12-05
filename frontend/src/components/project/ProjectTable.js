import * as React from 'react';
import axios from "axios";
import ManageTable from '../tool/ManageTable';
import { API_URL } from '../../config.js';
import ProjectControl from './ProjectControl';

function ProjectTable(props) {
    const [records, SetRescords] = React.useState([]);
    const theads = { 'id': 'ID', 'name': 'Name', 'dataset_count': 'Datasets', 'experiment_count': 'Experiments' };

    const getRecords = React.useCallback(() => {
        axios
            .get(API_URL + "project/list")
            .then(response => {
                if (response.data) {
                    SetRescords(response.data);
                }
            }, error => {
                if (error.response.data.msg) alert(error.response.data.msg);
                SetRescords([]);
            });
    }, []);

    React.useEffect(() => {
        getRecords();
    }, [getRecords]);

    const handleCreate = newName => {
        axios
            .post(API_URL + "project/create", { "name": newName })
            .then(response => {
                if (response.data) {
                    getRecords();
                }
            }, error => {
                if (error.response.data.msg) alert(error.response.data.msg);
                getRecords();
            });
    };

    return (
        <>
            <ManageTable title="My Projects" theads={theads} records={records} getRecords={getRecords} control={ProjectControl} create={handleCreate} />
        </>
    );
}


export default ProjectTable;
