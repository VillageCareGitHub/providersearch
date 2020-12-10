import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import Box from '@material-ui/core/Box';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import Badge from '@material-ui/core/Badge';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Link from '@material-ui/core/Link';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import NotificationsIcon from '@material-ui/icons/Notifications';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import Button from '@material-ui/core/Button';

//taken from other dashboard
import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
 
import DevButton from 'devextreme-react/button';
import DropDownBox from 'devextreme-react/drop-down-box';
//import { Lookup, DropDownOptions } from 'devextreme-react/lookup';

import DataSource from 'devextreme/data/data_source';
import ODataStore from 'devextreme/data/odata/store';
import ArrayStore from 'devextreme/data/array_store';
import LocalStore from 'devextreme/data/local_store';

import Select from "react-select";
import { DateBox } from 'devextreme-react/date-box';
import TextBox from 'devextreme-react/text-box';
import SelectBox from 'devextreme-react/select-box';

import PureModal from 'react-pure-modal';
import 'react-pure-modal/dist/react-pure-modal.min.css';
import CircularProgress from '@material-ui/core/CircularProgress';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogActions from '@material-ui/core/DialogActions';
import Dialog from '@material-ui/core/Dialog';




import DevDataGrid, {
  Column,
  Grouping,
  GroupPanel,
  Pager,
  Paging,
  FilterRow,
  Export,
  SearchPanel,
  Editing,
  Selection,
  Popup,
  Lookup,
  DropDownOptions,  
  RequiredRule,
  Form,
  Scrolling
} from 'devextreme-react/data-grid';
import { Item } from 'devextreme-react/form';
import DevTabPanel from 'devextreme-react/tab-panel';

import { PopupStuff } from 'devextreme-react/popup';

import apiCall from '../util/apiCall';


// nodejs library to set properties for components
import PropTypes from "prop-types";

import '../assets/css/popuptable.css'
// react plugin for creating charts
// import ChartistGraph from "react-chartist";
// @material-ui/core
import withStyles from "@material-ui/core/styles/withStyles";

import dashboardStyle from "../assets/jss/material-dashboard-react/views/dashboardStyle";
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import renderHTML from 'react-render-html';



const pageSizes = [5,10, 25, 50, 100,150,1000];

const searchparameters = [
  'Individual Provider',
  'Organization'
  
];




const labelStyle = { fill: '#BBDEFB' ,fontSize: 20,fontWeight: 'bold'};



const getPath = (x, width, y, y1) => `M ${x} ${y1}
   L ${width + x} ${y1}
   L ${width + x} ${y + 30}
   L ${x + width / 2} ${y}
   L ${x} ${y + 30}
   Z`;



function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24, // keep right padding when drawer closed
    background: 'orangered',
    
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  titleuser: {
    
    flexDirection: 'flex-end'
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing(7),
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(9),
    },
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'auto',
  },
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(2),
    
    display: 'flex',
    background: 'ghostwhite',
    overflow: 'auto',    
    flexDirection: 'column',
    width:'1500px',
    justifyContent:'center',
  },
  fixedHeight: {
    height: 135,
  },
}));

//old dashboard


export default function PROVIDERSEARCH() {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);  
  const handleDrawerOpen = () => {
    setOpen(true);
  };
  const handleDrawerClose = () => {
    setOpen(false);
  };
  const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);

  // from old dashboard
  const applyFilterTypes = [{
    key: 'auto',
    name: 'Immediately'
  }];

  

  
  const [usergrouphold,setusergrouphold]=React.useState(null);
  const [searchbyhold,setsearchbyhold]=React.useState(null);
  const [useridhold,setuseridhold]=React.useState(null);
  const [usernamehold,setusernamehold]=React.useState(null);
  const [membereffectivedatehold,setmembereffectivedatehold]=React.useState(null);
  const [memberlistdata,setmemberlistdata]=React.useState([]);
  const [membermeasuredata,setmembermeasuredata]=React.useState([]);
  const [memberplanid,setmemberplanid]=React.useState(null);
  const [selectmembereffectivedatehold,setselectmembereffectivedatehold]=React.useState(null);
  const [allSelectedRowsData,setallSelectedRowsData]=React.useState([]);
  const [searchdata,setsearchdata]=React.useState([]);
  const [measureyear,setmeasureyear]=React.useState([]);
  const [measureyeardata,setmeasureyeardata]=React.useState([]);
  const [memberlastname,setmemberlastname]=React.useState([]);
  const [memberfirstname,setmemberfirstname]=React.useState([]);
  const [memberdob,setmemberdob]=React.useState([]);
  const [providerdata,setproviderdata]=React.useState([]);
  const [providerspecialtydata,setproviderspecialtydata]=React.useState([]);
  const [measuresave,setmeasuresave]=React.useState([]);
  

  const [credstatus, setcredstatus] = React.useState(true); 
  const [mopen, setMOpen] = React.useState(false);

  const [modal, setModal] = React.useState(true);

  const [downloadbox, setdownloadbox] = React.useState(false);

  const [fromdate, setfromdate] = React.useState(null);
  const [todate, settodate] = React.useState(null);

  const [refreshlistenabled, setrefreshlistenabled] = React.useState(true);
  const [measurelistenabled, setmeasurelistenabled] = React.useState(true);
  const [saveinfoenabled, setsaveinfoenabled] = React.useState(true);
  const [gridBoxValue, setgridboxvalue] = React.useState([]);
  const [editRowKey, seteditRowKey] = React.useState(-1);
  const [cptrequired, setcptrequired] = React.useState('<p></p>');


  

  const handleClick = () => {
    setMOpen(true);
  };

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setMOpen(false);
  };

  const handleCancel = () => {
    setdownloadbox(false);
  };

  const handleOk = () => {
    getsupplmentaldata(fromdate,todate);
    //setdownloadbox(false);
    //need to put api for dowloading files based on dates
  };

  const downloadbuttonclick = () => {
    setdownloadbox(true);
  };


  // const [state, setState] = React.useState({
  //   mopen: false,
  //   vertical: 'top',
  //   horizontal: 'center',
  // });

  // const { vertical, horizontal} = state;

  // const handleClick = (newState) => () => {
  //   setState({ mopen: true, ...newState });
  // };

  // const handleClose = () => {
  //   setState({ ...state, mopen: false });
  // };
  const setcredentials=()=>{
      if (credstatus==true){
          getwindowsinfo();
          // getmemberyearlist();
          // getproviderlist();
          // getproviderspecialtylist();
          setcredstatus(false);
      }
  };
  

  const [showFilterRow,setshowFilterRow]=React.useState(true);
  const [showHeaderFilter,setshowHeaderFilter]=React.useState(true);
  const [currentFilter,setcurrentFiller]=React.useState(applyFilterTypes[0].key);

  const searchbyoptions=[{value:'1',label:'Enrollment Date'},
    {value:'2',label:'Medicare ID'},
    {value:'3',label:'Plan ID'},];

  const blockedates=[
    new Date("09/04/2020"),
    new Date("10/04/2020") ]
     
        
  const getwindowsinfo = () => {

                 setusergrouphold('SUPDB_USER');
                 setuseridhold('PROD');
                 setusernamehold('PROD');
                 setModal(false)

  //   const endpoint = "/api/supdb/authentication"
    
  //   const promise = apiCall(endpoint,'get')
  //   //console.log(endpoint)
  //  promise.then(blob=>blob.json()).then(json=>{
  //      console.log(json)
  //      console.log(json.data)
             
  //                setusergrouphold(json['usergroup']);
  //                setuseridhold(json['userid']);
  //                setusernamehold(json['username']);
  //                setModal(false)
                 
             
  //            /*alert(this.state.facilityhold)*/
  //    })
 }     

 const getmemberlist = () => {
    setModal(true); 
    console.log('trying to set modal box')
    const endpoint = "/api/fhir/practitionersearch"
    
    const promise = apiCall(endpoint,'post', {
      
        "provider":searchdata,
        "searchby":measureyear
        
        
      })
    //console.log(endpoint)
   promise.then(blob=>blob.json()).then(json=>{
       console.log(json)
       console.log('checking measure list')
       console.log(json.data)
       
                 
                 setmemberlistdata(json.data);
                 setModal(false);
                 
             
             /*alert(this.state.facilityhold)*/
     })
     //setModal(false)
     
     
 } 

 
  // Object.keys(memberlistdata.object).map((key, i) => (
  //   <p key={i}>
  //     <span>Key Name: {key}</span>
  //     <span>Value: {memberlistdata.object[key]}</span>
  //   </p>
  // )
//   const iterate = () => {
//     Object.keys(memberlistdata).forEach(key => {

//     console.log(`key: ${key}, value: ${memberlistdata[key]}`)

//     if (typeof memberlistdata[key] === 'object') {
//             iterate(memberlistdata[key])
//         }
//     })
// }
 

 const savememberinfo = () => {
  //alert('Measures Saved');
  handleClick();
  const endpoint = "/api/supdb/membersave"
  console.log(JSON.stringify(membermeasuredata))
  const promise = apiCall(endpoint,'post', {
    
      "data":JSON.stringify(membermeasuredata)
      
      
      
    })
  //console.log(endpoint)
 promise.then(blob=>blob.json()).then(json=>{
     console.log(json)
     console.log(json.output)
           
               setmeasuresave(json.output);
               
               
               
           
           /*alert(this.state.facilityhold)*/
   })
} 
 
 const getmemberyearlist = () => {

  const endpoint = "/api/supdb/getmeasureyear"
  
  const promise = apiCall(endpoint,'get')
  //console.log(endpoint)
 promise.then(blob=>blob.json()).then(json=>{
     console.log(json)
     console.log(json.data)
     console.log(json.data[0])
           
               setmeasureyeardata(json.data);
               
           
           /*alert(this.state.facilityhold)*/
   })
}

const getallsupplmentaldata = () => {

  const endpoint = "http://127.0.0.1:5000/api/supdb/downloadalldata"
  console.log('trying to initialize endpoint')
  //fetch(endpoint);
  fetch(endpoint,{
    method: 'GET',
    headers: {
      'Content-Type': 'text/plain',
    },
  }).then((response) => response.blob())
  .then((blob) => {
    // Create blob link to download
    const url = window.URL.createObjectURL(
      new Blob([blob]),
    );
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute(
      'download',
      'Inovalan_Non_Standard_Supplemental.txt',
    );

    // Append to html link element page
    document.body.appendChild(link);

    // Start download
    link.click();

    // Clean up and remove the link
    link.parentNode.removeChild(link);
  });
        
  console.log('ran function')
  setdownloadbox(false);
  
   //apiCall(endpoint,'get');
  //console.log(endpoint)
//  promise.then(blob=>blob.json()).then(json=>{
//      console.log(json)
//      console.log(json.data)
//      console.log(json.data[0])
           
              //  setmeasureyeardata(json.data);
               
           
           /*alert(this.state.facilityhold)*/
  
}

const getsupplmentaldata = (fromdate,todate) => {

  const data={
      
    "fromdate":fromdate,
    "todate":todate
    
  }
  const endpoint = "http://vcawswebdev:8091/api/supdb/downloaddata"
  console.log('trying to initialize endpoint')
  //fetch(endpoint);
  fetch(endpoint,{
    method: 'POST',
    body: JSON.stringify(data),
    mode: "cors",            
    headers: {
      'Content-Type': 'application/json',
    },
  }).then((response) => response.blob())
  .then((blob) => {
    // Create blob link to download
    const url = window.URL.createObjectURL(
      new Blob([blob]),
    );
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute(
      'download',
      'Inovalan_Non_Standard_Supplemental.txt',
    );

    // Append to html link element page
    document.body.appendChild(link);

    // Start download
    link.click();

    // Clean up and remove the link
    link.parentNode.removeChild(link);
  });
        
  console.log('ran function')
  setdownloadbox(false);
  
   //apiCall(endpoint,'get');
  //console.log(endpoint)
//  promise.then(blob=>blob.json()).then(json=>{
//      console.log(json)
//      console.log(json.data)
//      console.log(json.data[0])
           
              //  setmeasureyeardata(json.data);
               
           
           /*alert(this.state.facilityhold)*/
  
}

const getproviderlist = () => {

  const endpoint = "/api/supdb/providerlist"
  
  const promise = apiCall(endpoint,'get')
  //console.log(endpoint)
 promise.then(blob=>blob.json()).then(json=>{
     console.log(json)
     console.log(json.data)
     console.log(json.data[0])
           
               setproviderdata(json.data);
               
           
           /*alert(this.state.facilityhold)*/
   })
}

const getproviderspecialtylist = () => {

  const endpoint = "/api/supdb/providerspecialtylist"
  
  const promise = apiCall(endpoint,'get')
  //console.log(endpoint)
 promise.then(blob=>blob.json()).then(json=>{
     console.log(json)
     console.log(json.data)
     console.log(json.data[0])
           
               setproviderspecialtydata(json.data);
               
           
           /*alert(this.state.facilityhold)*/
   })
}     

 const getmembermeasureinfo = () => {

    const endpoint = "/api/supdb/membermeasure"
    
    const promise = apiCall(endpoint,'post', {
      
        "planid":memberplanid,        
        "measureyear":measureyear
      })
    //console.log(endpoint)
   promise.then(blob=>blob.json()).then(json=>{
       console.log(json)
       console.log(json.data)
       console.log(measureyear)
             
                 setmembermeasuredata(json.data);
                 setsaveinfoenabled(false);
                 
             
             /*alert(this.state.facilityhold)*/
     })
     
 }  
 
 const getproviderlistvalue= (search) => {

  const endpoint = "/api/supdb/membermeasure"
  
  const promise = apiCall(endpoint,'post', {
    
      "searchby":search       
      
    })
  //console.log(endpoint)
 promise.then(blob=>blob.json()).then(json=>{
     console.log(json)
     console.log(json.data)
     console.log(measureyear)
           
               setmembermeasuredata(json.data);
               
           
           /*alert(this.state.facilityhold)*/
   })
}     
       

  const griddatasource=new DataSource(memberlistdata);

  const measuregriddatasource=new DataSource(membermeasuredata);

  const lproviderdatasource={
    store: new ArrayStore({key: 'npi',
    data:providerdata}),
    
    paginate: true,
    pageSize: 10
};




  const lproviderspecialtydatasource={
    store: new ArrayStore({key: 'providerspecialty',
    data:providerspecialtydata}),
    
    paginate: true,
    pageSize: 10
};

  const onValueChanged=(e)=> {
      setsearchdata(e.value);
    
    };

  const onFromValueChanged=(e)=> {
      setfromdate(e.value);
    
    };

  const onToValueChanged=(e)=> {
      settodate(e.value);
    
    };

  const onSelectValueChanged=(e)=> {
      setmeasureyear(e.value);
      setrefreshlistenabled(false);
      console.log(e.value)

      
    
    };

  const convertDate=(d)=>{
        var parts = d.split(" ");
        var months = {Jan: "01",Feb: "02",Mar: "03",Apr: "04",May: "05",Jun: "06",Jul: "07",Aug: "08",Sep: "09",Oct: "10",Nov: "11",Dec: "12"};
        return parts[3]+"-"+months[parts[1]]+"-"+parts[2];
       };
       

  const onLookupValueChanged=(e)=> {
        e.value='10000000'
        
    }

  

    const onRowClick=(e)=> {

        // setmemberplanid('');
        // setmemberfirstname('');
        // setmemberlastname('');
        // setmemberdob('');
        setmembermeasuredata([]);
        setmemberplanid(e.values[2]);
        setmemberfirstname(e.values[0]);
        setmemberlastname(e.values[1]);
        // setmemberdob(convertDate(e.values[5].toString()));
        setmemberdob(e.values[5]);
        setmeasurelistenabled(false);
        setsaveinfoenabled(true);
        // getmembermeasureinfo();


        
        console.log(e.values)
        console.log(e.values[2])
        console.log(measureyear)
        // console.log(convertDate(e.values[6].toString()))
        // getmembermeasureinfo();
       //  alert(e.selectedRowsData[0]);
       
   }

   const onRowDblClick=(e)=> {
    setmemberplanid(e.values[3]);
    setselectmembereffectivedatehold(convertDate(e.values[6].toString()));
    console.log(e.values)
    console.log(e.values[3])
    console.log(convertDate(e.values[6].toString()))
    getmembermeasureinfo();
   //  alert(e.selectedRowsData[0]);
   
}
const dataGridRender=()=> {
  return (
    <DevDataGrid
      dataSource={providerdata}
      
      hoverStateEnabled={true}
      keyExpr="npi"
      selectedRowKeys={gridBoxValue}
      onSelectionChanged={dataGrid_onSelectionChanged}
      >
      <Selection mode="multiple" />
      <Scrolling mode="infinite" />
      <Paging enabled={true} pageSize={10} />
      <FilterRow visible={true} />
    </DevDataGrid>
  );
}

const syncDataGridSelection=(e)=> {
  console.log(e.value)
  setgridboxvalue(e.value);
}

const dataGrid_onSelectionChanged=(e)=> {
  console.log(e.selectedRowKeys.length && e.selectedRowKeys)
  console.log(e.selectedRowKeys)
  setgridboxvalue(e.selectedRowKeys);
}
    
  
 
// {"fields":[{"name":"plan_id","type":"string"},
// {"name":"provider_npi","type":"string"},{"name":"provider_id","type":"string"},
// {"name":"hicn_mbi","type":"string"},{"name":"cin","type":"string"},{"name":"lob","type":"string"},
// {"name":"member_last_name","type":"string"},{"name":"member_first_name","type":"string"},
// {"name":"member_dob","type":"string"},{"name":"member_effective_date","type":"string"},
// {"name":"provider_last_name","type":"string"},{"name":"provider_first_name","type":"string"}],"pandas_version":"0.20.0"},

  const gridinfo=(<DevDataGrid
    dataSource={griddatasource}
    allowColumnReordering={true}
    allowColumnResizing={true}
    showBorders={true}
    showRowLines={true}
    onRowClick={onRowClick}
    // onSelectionChanged={onSelectionChanged}
    // onRowDblClick={onRowDblClick}
    
    
    
    
  >
    <Export enabled={true} fileName="VILLAGECAREMAX_Provider_List" allowExportSelectedData={true} />
    <FilterRow visible={showFilterRow}
        applyFilter={currentFilter} />
    <GroupPanel visible={true} />
    <SearchPanel visible={true} highlightCaseSensitive={true} />
    <Selection mode="single" />
    <Grouping autoExpandAll={true} expandMode="rowClick"/>
    
            
    
    <Column dataField="specialty" caption="Specialty" width="150" dataType="string"  /> 
    <Column dataField="provider_id" caption="Provider ID" width="150" dataType="string"  /> 
    <Column
      dataField="name"
      caption="Provider Name"
      dataType="string"
      width="200"
      
      
    />
    <Column
      dataField="gender"
      caption="Gender"
      width="100"
      dataType="string"
      
      
    />
    
    <Column dataField="address" caption="Address" width="450" dataType="string"  />
    <Column dataField="phone" caption="Contact" width="100" dataType="string"  /> 
    <Column dataField="lob" caption="LOB" dataType="string"  />
     
    {/* <Column dataField="cin" caption="Medicaid ID" dataType="string"  />
    <Column dataField="member_dob" caption="DOB" dataType="string" visible={true} /> 
    <Column dataField="lob" caption="LOB" dataType="string"  />
    <Column dataField="member_effective_date" caption="Member Effective Date" dataType="date"  />
    <Column dataField="provider_npi" caption="Provider NPI" dataType="string"  /> 
    <Column dataField="provider_first_name" caption="Provider First name" dataType="string"  />  
    <Column dataField="provider_last_name" caption="Provider Last Name" dataType="string"  />  */}
       
           

    <Pager allowedPageSizes={pageSizes} showPageSizeSelector={true} />
    <Paging defaultPageSize={50} />
  </DevDataGrid>)

// {"fields":[{"name":"member_measure_id","type":"integer"},
// {"name":"plan_id","type":"string"},
// {"name":"provider_id","type":"string"},
// {"name":"measure","type":"string"},
// {"name":"dos","type":"string"},
// {"name":"cptpx","type":"string"},
// {"name":"hcpcspx","type":"string"},{"name":"loinc","type":"string"},{"name":"snomed","type":"string"},
// {"name":"cvx","type":"string"},{"name":"cptcatII","type":"string"},{"name":"icd10x","type":"string"},
// {"name":"ubrev","type":"string"},{"name":"providerspecialty","type":"string"},{"name":"results","type":"string"},
// {"name":"measure_year","type":"integer"},{"name":"create_date","type":"datetime"},{"name":"modified_date","type":"datetime"},
// {"name":"create_user_id","type":"string"},{"name":"modified_user_id","type":"string"},{"name":"measure_description","type":"string"}],"pandas_version":"0.20.0"}

const reqrule=(<RequiredRule />)
var cptReqRule=(<p></p>)
const dataGridRef = React.createRef();
const rdataGrid={get dataGrid() {
  return dataGridRef.current.instance;
}
}
const getCellValue=()=> {
  const editRowIndex = rdataGrid.getRowIndexByKey(editRowKey);
  if(editRowIndex >= 0) {
      return rdataGrid.cellValue(editRowIndex, "measure_rules");
  }
  return null;
}
//establishing required rules
const onEditorPreparing=(e)=>{
  e.cancel=true
//   if(e.dataField === "cptpx" && e.parentType ==="dataRow"){
//   //console.log(String(e.key['measure_rules']))
//     console.log(e.key)
// }
}

const onEditorPrepared=(e)=>{
  
  if(e.dataField === "cptpx" && e.parentType ==="dataRow"){
  //console.log(String(e.key['measure_rules']))
    e.setValue('','')
    
  }
  if(e.dataField === "cptcatII" && e.parentType ==="dataRow"){
    //console.log(String(e.key['measure_rules']))
      e.setValue('','')
      
  }
  if(e.dataField === "loinc" && e.parentType ==="dataRow"){
      //console.log(String(e.key['measure_rules']))
      e.setValue('','')
        
  }
  if(e.dataField === "icd10x" && e.parentType ==="dataRow"){
    //console.log(String(e.key['measure_rules']))
    e.setValue('','')
      
  }
  if(e.dataField === "snomed" && e.parentType ==="dataRow"){
        //console.log(String(e.key['measure_rules']))
      e.setValue('','')
          
  }

  if(e.dataField === "cvx" && e.parentType ==="dataRow"){
          //console.log(String(e.key['measure_rules']))
      e.setValue('','')
            
  }
  if(e.dataField === "ubrev" && e.parentType ==="dataRow"){
          //console.log(String(e.key['measure_rules']))
      e.setValue('','')
            
  }
  if(e.dataField === "providerspecialty" && e.parentType ==="dataRow"){
    //console.log(String(e.key['measure_rules']))
      e.setValue('','')
      
  }
  if(e.dataField === "results" && e.parentType ==="dataRow"){
    //console.log(String(e.key['measure_rules']))
      e.setValue('','')
      
  }
}

const onEditingStart=(e)=> {
    //seteditRowKey(e.key);
    
     

    
    

  
  // ...
}
// CPT
// CPTII
// PROVIDERSPECIALTY
// ICD

const onRowUpdating=(e)=> {
  console.log(e.key['measure_rules'])
    var newarr=String(e.key['measure_rules']).split(",")
    var i=0
    var len=0
    var text=""
    var msg=""
    e.cancel=false
    for (i = 0, len = newarr.length, text = ""; i < len; i++) {
        text = newarr[i]
        if(String(text)=='CPT'){
          
          console.log(String(e.newData['cptpx']))
          if(typeof e.newData['cptpx']!=undefined && String(e.newData['cptpx'])===''){
            
            e.cancel=true
            msg+='You need to enter a cpt code\r'
            //alert('You need to enter a cpt code');
              console.log('checking cptpx field')
          }
          
          console.log('CPT is now required');
          console.log(e.newData)
          
        }

        if(String(text)=='CPTII'){
          
          console.log(String(e.newData['cptcatII']))
          if(typeof e.newData['cptcatII']!=undefined && String(e.newData['cptcatII'])===''){
            
            e.cancel=true
            msg+='You need to enter a cpt cat II code\r'
            //alert('You need to enter a cpt cat II code');
              console.log('checking cpt cat II field')
          }
          
          console.log('CPTII is now required');
          console.log(e.newData)
          
        }

        if(String(text)=='PROVIDERSPECIALTY'){
          
          console.log(String(e.newData['providerspecialty']))
          if(typeof e.newData['providerspecialty']!=undefined && String(e.newData['providerspecialty'])===''){
            
            e.cancel=true
            msg+='You need to enter a provider specialty information\r'
            //alert('You need to enter a cpt cat II code');
              console.log('checking cpt cat II field')
          }
          
          console.log('PROVIDERSPECIALTY is now required');
          console.log(e.newData)
          
        }

        if(String(text)=='ICD'){
          
          console.log(String(e.newData['icd10x']))
          if(typeof e.newData['icd10x']!=undefined && String(e.newData['icd10x'])===''){
            
            e.cancel=true
            msg+='You need to enter a ICD 10 code\r'
            //alert('You need to enter a cpt cat II code');
              console.log('checking icd 10 field')
          }
          
          console.log('ICD 10 is now required');
          console.log(e.newData)
          
        }

        if(String(text)=='LOINC'){
          
          console.log(String(e.newData['loinc']))
          if(typeof e.newData['loinc']!=undefined && String(e.newData['loinc'])===''){
            
            e.cancel=true
            msg+='You need to enter a loinc code\r'
            //alert('You need to enter a cpt cat II code');
              console.log('checking loinc field')
          }
          
          console.log('loinc is now required');
          console.log(e.newData)
          
        }

        if(String(text)=='SNOMED'){
          
          console.log(String(e.newData['snomed']))
          if(typeof e.newData['snomed']!=undefined && String(e.newData['snomed'])===''){
            
            e.cancel=true
            msg+='You need to enter a snomed code\r'
            //alert('You need to enter a cpt cat II code');
              console.log('checking snomed field')
          }
          
          console.log('snomed is now required');
          console.log(e.newData)
          
        }

        if(String(text)=='CVX'){
          
          console.log(String(e.newData['cvx']))
          if(typeof e.newData['cvx']!=undefined && String(e.newData['cvx'])===''){
            
            e.cancel=true
            msg+='You need to enter a cvx code\r'
            //alert('You need to enter a cpt cat II code');
              console.log('checking cvx field')
          }
          
          console.log('cvx is now required');
          console.log(e.newData)
          
        }

        if(String(text)=='UBREV'){
          
          console.log(String(e.newData['ubrev']))
          if(typeof e.newData['ubrev']!=undefined && String(e.newData['ubrev'])===''){
            
            e.cancel=true
            msg+='You need to enter a ubrev code\r'
            //alert('You need to enter a cpt cat II code');
              console.log('checking ubrev field')
          }
          
          console.log('ubrev is now required');
          console.log(e.newData)
          
        }

        if(String(text)=='RESULTS'){
          
          console.log(String(e.newData['results']))
          if(typeof e.newData['results']!=undefined && String(e.newData['results'])===''){
            
            e.cancel=true
            msg+='You need to enter a results code\r'
            //alert('You need to enter a cpt cat II code');
              console.log('checking results field')
          }
          
          console.log('results is now required');
          console.log(e.newData)
          
        }

        //put more code here for required rules
        
        
    }

    //all messages
    if(msg!=''){
      alert(msg)
    }  

}

const onRowInserting=(e)=> {
console.log('inserting now')

}
//measure grid
const measuregrid=(<DevDataGrid
  dataSource={measuregriddatasource}
  allowColumnReordering={true}
  showBorders={true}
  showRowLines={true}
  rowAlternationEnabled={true}
  onRowUpdating={onRowUpdating}
  //onRowInserting={onRowInserting}
  //onEditingStart={onEditingStart}
  //onEditorPreparing={onEditorPreparing}
  onEditorPrepared={onEditorPrepared}

  ref={dataGridRef}
  
  
  
  
>
  
  <FilterRow visible={showFilterRow}
      applyFilter={currentFilter} />           
  
  <Editing
                  allowUpdating={true}                   
                  
                  mode="popup" >
          <Popup title="Measure Detail" showTitle={true} width="1100" height="900">
          
          
          </Popup>
          
          <Form>
          
          <Item itemType="group" colCount={1} colSpan={1}>
          
          <Item dataField="plan_id" 
          
          editorOptions={{ readOnly: true }}
          />

          <Item dataField="measure" 
          
          editorOptions={{ readOnly: true }}
          />
            
          <Item dataField="measure_description" 
          
          editorOptions={{ readOnly: true }}
          />

          <Item dataField="provider_id" 
          
          editorOptions={{ readOnly: false,showClearButton:true,width:800 }}
          />
         

          <Item dataField="dos" 
          
          editorOptions={{ readOnly: false }}
          />
          <Item dataField="cptpx" 
          
          editorOptions={{ readOnly: false }}
          />
          <Item dataField="loinc" 
          
          editorOptions={{ readOnly: false }}
          />
          <Item dataField="icd10x" 
          
          editorOptions={{ readOnly: false }}
          />
          <Item dataField="snomed" 
          
          editorOptions={{ readOnly: false }}
          />
          <Item dataField="cvx" 
          
          editorOptions={{ readOnly: false }}
          />
          <Item dataField="cptcatII" 
          
          editorOptions={{ readOnly: false }}
          />
          <Item dataField="ubrev" 
          
          editorOptions={{ readOnly: false }}
          />
          <Item dataField="providerspecialty" 
          
          editorOptions={{ readOnly: false,showClearButton:true,width:800  }}
          />
          <Item dataField="results" 
          
          editorOptions={{ readOnly: false }}
          />
          </Item>
          
          </Form>

  </Editing>
  
  <Column
    dataField="plan_id"
    caption="Plan ID"
    dataType="string"
    enabled={false}
    visible={false}
    
    
  />
  
  <Column
    dataField="measure"
    caption="Measure"
    dataType="string"
    enabled={false}
    visible={false}
    
    
  />
  <Column
    dataField="measure_description"
    caption="Measure Description"
    dataType="string"
    width="550"
    enabled={false}
    editorOptions={{height: 30 }}
    
    
  />
  
  <Column
    dataField="provider_id"
    caption="Servicing Provider NPI"
    dataType="string"
    visible={false}
    
    
    
    
  ><RequiredRule /><Lookup dataSource={lproviderdatasource} valueExpr="npi" displayExpr="prov_provider_name_and_address" keyExpr="npi" placeholder="Select Provider Info"
  
  showClearButton={true}
  
  /></Column>
  <Column dataField="dos" caption="DOS" dataType="date">   
   {reqrule}</Column>
   <Column dataField="cptpx" caption="CPT Code" dataType="string"  ></Column>
  <Column
    dataField="loinc"
    caption="LOINC"
    dataType="string"
    visible={false}
    
    
  />
  <Column dataField="icd10x" caption="ICD Code" dataType="string"  />
  <Column
    dataField="snomed"
    caption="SNOMED"
    dataType="string"
    visible={true}
    
  />
  <Column dataField="cvx" caption="CVX" dataType="string" visible={false}  />
  <Column dataField="cptcatII" caption="CPT CAT II" dataType="string" visible={true}  />
  <Column dataField="ubrev" caption="UBREV" dataType="string" visible={false}  />
  <Column dataField="providerspecialty" caption="PROVIDER SPECIALTY" dataType="string" visible={true}  >
  <Lookup dataSource={lproviderspecialtydatasource} valueExpr="providerspecialty" displayExpr="provspecdes" keyExpr="providerspecialty" placeholder="Select Provider Specialty Info"
  
  showClearButton={true}
  
  /></Column>
  <Column dataField="results" caption="Results" dataType="string" visible={false}  />
  
  
  
  
    
         

  <Pager allowedPageSizes={pageSizes} showPageSizeSelector={true} />
  <Paging defaultPageSize={10} />
</DevDataGrid>)




  

 

 
    


  return (      
    <div className={classes.root}>
    <Snackbar open={mopen} autoHideDuration={2000} onClose={handleClose} anchorOrigin={ {vertical: 'top', horizontal: 'center' }} >
        <Alert onClose={handleClose} severity="success"  >
          Measures Saved
        </Alert>
      </Snackbar>
        {setcredentials()}
        
        
      <CssBaseline />
      <AppBar position="absolute"  className={clsx(classes.appBar, open && classes.appBarShift)}>
        <Toolbar className={classes.toolbar}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            className={clsx(classes.menuButton, open && classes.menuButtonHidden)}
          >
            <MenuIcon />
          </IconButton>
          <Typography component="h1" variant="h6" color="inherit" noWrap className={classes.title}>
            VILLAGECAREMAX PROVIDER SEARCH
          </Typography>
          
          {/* <Typography component="h1" variant="h6" color="inherit" noWrap className={classes.title}>
            
            SECURITY GROUP: {usergrouphold}
          </Typography> */}
          
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        classes={{
          paper: clsx(classes.drawerPaper, !open && classes.drawerPaperClose),
        }}
        open={open}
      >
        <div className={classes.toolbarIcon}>
          <IconButton onClick={handleDrawerClose}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <Divider />
        <List></List>
        <Divider />
        <List></List>
      </Drawer>
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <Container maxWidth="lg" className={classes.container}>
          <Grid container spacing={2}>
            {/* Chart */}
            <Grid item xs={12} md={12} lg={12}>
              <Paper className={fixedHeightPaper}>
              <div className='CREDHEADER'>
              {/* <div className='CRED'><label>User Name: {usernamehold}</label></div>
              <div className='CRED'><label>Security User Group: {usergrouphold}</label></div> */}
              
              <div className='BANMEASUREYEAR'><label>Search By</label>
            <SelectBox 
            items={searchparameters}
            placeholder="Select Search"
            // defaultValue={measureyeardata[0]}
            // value={measureyeardata[0]}
            onValueChanged={onSelectValueChanged} 
            
            />
           
            </div> 
            <div className='BAN'><label>Enter Provider/Organization</label><TextBox placeholder="Enter Provider or Organization" 
                showClearButton={true}                
                onValueChanged={onValueChanged}
                // inputAttr="{autocomplete='off'}"
                
                /></div>
             
             
            <div className='BAN1'>
            <DevButton
                text="Search"
                onClick={getmemberlist}
                type="default"
                stylingMode="contained"
                disabled={refreshlistenabled}
                width="300"
                
                />
            </div>  
            </div>
            <div className='HEADERBAN'>
              
              {/* <div className='BAN'><label>Select Search Criteria</label><Select id="searchby" placeholder='SELECT SEARCH BY'
                  options={searchbyoptions} >Search By</Select></div> */}
                
           
            
            
          </div>
              </Paper>
            </Grid>
           
            {/* Recent Orders */}
            <Grid item xs={20} md={20} lg={20}>
              <Paper className={classes.paper}>
                 
                 <div>{gridinfo}</div>
                 {/* <div className="SHOWMEASUREBUTTONHEADER">
                 <div className="SHOWMEASUREBUTTON"> 
              <DevButton
                text="Show Measures"
                onClick={getmembermeasureinfo}
                visible={true}
                disabled={measurelistenabled}
                type="default"
                stylingMode="contained"
                /> 
              
                </div>
                </div> */}
              </Paper>
            </Grid>
            {/* <Grid item xs={20} md={20} lg={20}>
              <Paper className={classes.paper}>
              <div className='CREDHEADER'>
              <div className='CRED'><label>Member Last Name: {memberlastname}</label></div>
              <div className='CRED'><label>Member First Name: {memberfirstname}</label></div>
              <div className='CRED'><label>Member DOB: {memberdob}</label></div>
              </div> 
                {measuregrid}
                <div className="SHOWMEASUREBUTTONHEADER">  
                <div className="SHOWMEASUREBUTTON">   
               <DevButton
                text="Save Information"
                onClick={savememberinfo}
                disabled={saveinfoenabled}
                type="default"
                stylingMode="contained"
                /> 
                </div>
                </div>
                 
              </Paper>
            </Grid> */}
          </Grid> 
          <Box pt={4}>
            
          </Box>
          <PureModal
              header="Retrieving Provider Information"
              closeButton=''
              isOpen={modal}
              width='600px'
                         
              
            >
              <div className="progressbar"><CircularProgress /></div>
          </PureModal>
          <Dialog
      disableBackdropClick
      disableEscapeKeyDown
      maxWidth="xs"
      
      aria-labelledby="confirmation-dialog-title"
      open={downloadbox}
      
    >
      <DialogTitle id="confirmation-dialog-title">Download Non Standard Supplemental File</DialogTitle>
      <DialogContent dividers>
        {/* need content here */}
        <div className="DOWNLOADBUTTON">
        <label>Entry From Date</label>
              <DateBox
                onValueChanged={onFromValueChanged} 
                type="date" />
            </div>
            <div className="DOWNLOADBUTTON">
            <label>Entry To Date</label>
              <DateBox
                onValueChanged={onToValueChanged} 
                type="date" />
            </div>
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={handleCancel} color="primary">
          Cancel
        </Button>
        <Button onClick={handleOk} color="primary">
          Ok
        </Button>
      </DialogActions>
    </Dialog>
        </Container>
      </main>
    </div>
  );
}