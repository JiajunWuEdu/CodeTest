import * as React from 'react';
import axios from "axios";
import ManageTable from '../tool/ManageTable';
import { API_URL } from '../../config.js';
import DatasetControl from './DatasetControl';

function DatasetTable({ projectId }) {
    const [records, SetRescords] = React.useState([]);
    const theads = { 'id': 'ID', 'name': 'Name', 'row_count': 'Rows', 'upload_time': 'Upload Time' };
    
    const getRecords = React.useCallback(() => {
        axios
            .get(API_URL + "project/datasets?id=" + projectId)
            .then(response => {
                if (response.data) {
                    SetRescords(response.data);
                }
            }, error => {
                if (error.response.data.msg) alert(error.response.data.msg);
                SetRescords([]);
            });
    }, [projectId]);

    React.useEffect(() => {
        getRecords();
    }, [getRecords]);

    const handleCreate = newName => {
        axios
            .post(API_URL + "dataset/create", { "name": newName, "project_id": projectId })
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
            <ManageTable title="Datasets" theads={theads} records={records} getRecords={getRecords} control={DatasetControl} create={handleCreate} />
        </>
    );
}


export default DatasetTable;
