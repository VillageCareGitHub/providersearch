import time

import requests
import pandas as pd
import json

#https://vc202011.aidbox.app/fhir/Practitioner?name=SUMIR&active=false
#ENDPOINT='https://vc202011.aidbox.app/fhir'
ENDPOINT='https://vc202011dev.aidbox.app/fhir'
#ENDPOINT='https://vc202011.aidbox.app/'
CALL_PROVIDER_NAME='/Practitioner?name={provider}'
CALL_PROVIDER_NAME_FAST='/PractitionerRole?_include=PractitionerRole:organization&_include=PractitionerRole:practitioner&_include=PractitionerRole:network&_include=PractitionerRole:location&_include=PractitionerRole:healthcareService&practitionerActive=true&practitionerName={practitionerName}'
CALL_PROVIDER_ALL='/Practitioner?active=true'
CALL_ORGANIZATION='/Organization?name={provider}'
CALL_ORGANIZATION_FAST='/OrganizationAffiliation?_include=OrganizationAffiliation:organization&_include=OrganizationAffiliation:network&organizationActive=true&organizationName={organizationName}'
CALL_ALL_PRACTIONER_INFO='/PractitionerRole?_include=PractitionerRole:organization&_include=PractitionerRole:practitioner&_include=PractitionerRole:network&_include=PractitionerRole:location&_include=PractitionerRole:healthcareService&practitioner:Practitioner.active=true&practitioner:Practitioner.name={provider}'





def json_demo(name,address,phone,gender):
    return {"name":name,
            "address":address,
            "phone":phone,
            "gender":gender}

def get_api_organization_id(jvalue):
    data_hold=[]
    data_id_hold=[]
    d_bool=False
    d_id=''
    d_name=''
    for nkey,nvalues in jvalue.items():
        for lkey,lvalues in nvalues.items():
            #print(lkey)
            if lkey=='resourceType':
                #print('did i get resourcetype')
                h_resourcetype=lvalues
                #print(lvalues)

            if lkey=='name':
                d_name=lvalues

            if lkey=='id':
                if h_resourcetype=='Organization' and d_bool==False:
                    #print(lvalues)
                    d_id=lvalues
                    #print(d_id)
                    dstr={"d_id":d_id,
                          "name":d_name,
                          "lob":'',
                          "lobname":'',
                          "specialty":''}
                    data_hold.append(dstr)
                    #d_bool==True
    # create dataframe
    id_df=pd.DataFrame(data_hold)

    return id_df

def get_api_org_demographics(organizationid):
    CALL_PRACTITIONER_ID='/Organization?id={organizationid}'
    data_hold=[]
    d_name=''
    gender_name='NA'
    specialty=''
    response=requests.get(ENDPOINT+CALL_PRACTITIONER_ID.format(organizationid=organizationid))
    if response.status_code==200:
        for key,values in response.json().items():
            #print(key)
            #print(values)
            if key=='entry':
                t=pd.DataFrame(values)
                if response.text.find('"resource":')!=-1:
                    for akey,avalue in t['resource'].items():
                        #print(avalue)
                        for nkey,nvalue in avalue.items():
                            if nkey=='name':
                                d_name='{0}'.format(nvalue)

                            if nkey=='gender':
                                gender_name='{0}'.format('NA')

                            # if nkey=='qualification':
                            #     specialty='{0}'.format(str(nvalue[0]['code']['coding'][0]['display']).strip())




                        jstr={"d_id":organizationid,
                                "name":d_name,
                                "gender":gender_name}

                        data_hold.append(jstr)
        #creating dataframe
        demo_df=pd.DataFrame(data_hold)
        return demo_df

    else:

        #creating dataframe
        return {"data":[]}

def get_api_org_location(organizationid):
    CALL_PRACTITIONER_ID='/Organization?id={organizationid}'
    data_hold=[]
    d_address=''
    d_phone=''
    n=-1
    nd=-1
    response=requests.get(ENDPOINT+CALL_PRACTITIONER_ID.format(organizationid=organizationid))
    if response.status_code==200:
        for key,values in response.json().items():
            #print(key)
            #print(values)
            if key=='entry':
                t=pd.DataFrame(values)
                if response.text.find('"resource":')!=-1:
                    for akey,avalue in t['resource'].items():
                        #print(avalue)
                        for nkey,nvalue in avalue.items():
                            if nkey=='address':
                                if nvalue!=[]:

                                    for i in range(len(nvalue)):
                                        n+=1
                                        if str(nvalue[n]).find('postalCode')!=-1:
                                            d_address='{0} {1}, {2} {3}'.format(str(nvalue[n]['line'][0]).strip(),str(nvalue[n]['city']).strip(),nvalue[n]['state'],str(nvalue[n]['postalCode'])[0:5]+'-'+str(nvalue[n]['postalCode'])[5:])
                                        else:
                                            d_address='{0} {1}, {2} {3}'.format(str(nvalue[n]['line'][0]).strip(),str(nvalue[n]['city']).strip(),nvalue[n]['state'],'')
                                        jstr={"d_id":organizationid,
                                        "addrid":n,
                                        "address":d_address}

                                        data_hold.append(jstr)

                                else:
                                    d_address='{0} {1} {2} {3}'.format('','','','')
                                    jstr={"d_id":organizationid,
                                        "addrid":0,
                                        "address":d_address}

                                    data_hold.append(jstr)

                        #     if nkey=='telecom':
                        #         print(nvalue)
                        #         if nvalue!=[]:
                        #             for d in range(len(nvalue)):
                        #                 nd+=1
                        #                 d_phone='{0}'.format(nvalue[nd]['value'])




                        # jstr={"d_id":organizationid,
                        #         "address":d_address,
                        #         "phone":d_phone}

                        # data_hold.append(jstr)
                else:
                    jstr={"d_id":organizationid,
                                "addrid":0,
                                "address":'',
                                "phone":''}

                    data_hold.append(jstr)
        #creating dataframe
        demo_df=pd.DataFrame(data_hold)
        if data_hold!=[]:
            new_demo_df=demo_df.drop_duplicates()
            return new_demo_df
        else:
            return demo_df

    else:

        #creating dataframe
        return {"data":[]}

def get_api_org_phone(organizationid):
    CALL_PRACTITIONER_ID='/Organization?id={organizationid}'
    data_hold=[]
    d_address=''
    d_phone=''
    n=-1
    nd=-1
    response=requests.get(ENDPOINT+CALL_PRACTITIONER_ID.format(organizationid=organizationid))
    if response.status_code==200:
        for key,values in response.json().items():
            #print(key)
            #print(values)
            if key=='entry':
                t=pd.DataFrame(values)
                if response.text.find('"resource":')!=-1:
                    for akey,avalue in t['resource'].items():
                        #print(avalue)
                        for nkey,nvalue in avalue.items():


                            if nkey=='telecom':
                                print(nvalue)
                                if nvalue!=[]:
                                    for d in range(len(nvalue)):
                                        nd+=1
                                        d_phone='{0}'.format(nvalue[nd]['value'])

                                        jstr={"d_id":organizationid,
                                                "addrid":nd,
                                                "phone":d_phone}

                                        data_hold.append(jstr)
                                else:
                                    jstr={"d_id":organizationid,
                                                "addrid":0,
                                                "phone":d_phone}

                                    data_hold.append(jstr)

                else:
                    jstr={"d_id":organizationid,
                    "addrid":0,
                    "phone":d_phone}

                    data_hold.append(jstr)
        #creating dataframe
        demo_df=pd.DataFrame(data_hold)
        if data_hold!=[]:
            new_demo_df=demo_df.drop_duplicates()
            return new_demo_df
        else:
            return demo_df

    else:

        #creating dataframe
        return {"data":[]}


def get_demographics(jvalue,searchby):
    d_id=''
    d_name=''
    gender_name='NA'
    dc=False
    data_hold=[]
    for dkey,dvalues in jvalue.items():
        if dkey=='name':
            if searchby=='Organization':
                d_name='{0}'.format(dvalues)
            else:
                d_name='{0} {1}'.format(dvalues[0]['given'][0],dvalues[0]['family'])

        if dkey=='gender':
            if searchby=='Organization':
                gender_name='{0}'.format('N/A')
            else:
                gender_name='{0}'.format(dvalues).upper()


        if dkey=='id':
            d_id='{0}'.format(dvalues)
            dc=True

        if dc==True:
            jstr={"d_id":d_id,
                  "name":d_name,
                  "gender":gender_name,
                  "lob":'',
                  "spec_id":0,
                  "specialty":''}
            data_hold.append(jstr)
            dc=False

    #creating dataframe
    demo_df=pd.DataFrame(data_hold)


    return demo_df

def get_address(jvalue,searchby):
    d_id=''
    d_address=''
    dc=False
    data_hold=[]
    data_id_hold=[]
    d_len=0
    for dkey,dvalues in jvalue.items():
        if dkey=='address':
           if dvalues!=[]:
                d_len=len(dvalues)
                for i in range(d_len):
                    d_address='{0} {1}, {2} {3}'.format(dvalues[i]['line'][0],dvalues[i]['city'],dvalues[i]['state'],str(dvalues[i]['postalCode'])[0:5]+'-'+str(dvalues[i]['postalCode'])[5:])
                    jstr={"addr_id":i,
                          "address":d_address}
                    data_hold.append(jstr)
           else:
                d_address='{0} {1} {2} {3}'.format('','','','')
                jstr={"addr_id":0,
                      "address":d_address}
                data_hold.append(jstr)

        if dkey=='id':
            if dvalues!=[]:
                d_len=len(dvalues)
                for ii in range(d_len):
                    d_id='{0}'.format(dvalues)
                    istr={"addr_id":ii,
                          "d_id":d_id}
                    data_id_hold.append(istr)

            else:
                d_id='{0}'.format('0')
                istr={"addr_id":0,
                          "d_id":d_id}
                data_id_hold.append(istr)



    # creating dataframe
    d_id_df=pd.DataFrame(data_id_hold)
    address_df=pd.DataFrame(data_hold)

    # print(d_id_df)
    # print(address_df)

    # merging dataframes
    if data_hold!=[]:
        new_address_df=pd.merge(address_df,d_id_df,on='addr_id')
        return new_address_df
    else:
       return address_df




def get_phone(jvalue,searchby):
    d_id=''
    d_phone=''
    dc=False
    data_hold=[]
    data_id_hold=[]
    d_len=0
    p_len=0
    for dkey,dvalues in jvalue.items():
        if dkey=='telecom':
           if dvalues!=[]:
                d_len=len(dvalues)
                p_len=d_len
                #print(d_len)
                for i in range(d_len):
                    d_phone=phone='{1}'.format(dvalues[i]['system'],dvalues[i]['value'])
                    jstr={"addr_id":i,
                          "phone":d_phone}
                    data_hold.append(jstr)
           else:
                d_phone='{0} {1} {2} {3}'.format('','','','')
                jstr={"addr_id":0,
                      "phone":d_phone}
                data_hold.append(jstr)

        if dkey=='id':
            if dvalues!=[]:
                d_len=len(dvalues)
                #print(p_len)
                for ii in range(d_len):
                    d_id='{0}'.format(dvalues)
                    istr={"addr_id":ii,
                          "d_id":d_id}
                    data_id_hold.append(istr)



    # creating dataframe
    d_id_df=pd.DataFrame(data_id_hold)
    #print(d_id_df)
    phone_df=pd.DataFrame(data_hold)
    #print(phone_df)

    # merging dataframes
    new_phone_df=pd.merge(phone_df,d_id_df,on='addr_id')

    return new_phone_df


def get_practitioner_id(jvalue):
    data_hold=[]
    data_id_hold=[]
    d_bool=False
    d_id=''
    d_name=''
    prov_id=''
    for nkey,nvalues in jvalue.items():
        for lkey,lvalues in nvalues.items():
            #print(lkey)
            if lkey=='resourceType':
                #print('did i get resourcetype')
                h_resourcetype=lvalues
                #print(lvalues)

            if lkey=='name':
                d_name=lvalues

            if lkey=='id':
                if h_resourcetype=='Practitioner' and d_bool==False:
                    #print(lvalues)
                    d_id=lvalues
                    #print(d_id)


            if lkey=='identifier':
                if h_resourcetype=='Practitioner':
                    print('provider id')
                    print(lvalues)
                    for pp in range(len(lvalues)):
                        print('checking provider id info')
                        if str(lvalues[pp]).find('PROVIDER_ID')!=-1:
                            print('found provider id')
                            print(lvalues[pp]['value'])
                            prov_id=lvalues[pp]['value']
                    dstr={"d_id":d_id,
                          "name":d_name,
                          "provider_id":prov_id}
                    data_hold.append(dstr)

                    #d_bool==True
    # create dataframe
    id_df=pd.DataFrame(data_hold)

    return id_df


def get_specialty(jvalue,d_id):
    h_resource=False
    h_name=''
    h_resourcetype=''

    data_hold=[]
    data_id_hold=[]
    for nkey,nvalues in jvalue.items():
        for lkey,lvalues in nvalues.items():
            #print(lkey)
            if lkey=='resourceType':
                #print('did i get resourcetype')
                h_resourcetype=lvalues
                #print(lvalues)
                if lvalues=='HealthcareService' and h_name!='':
                    #print(h_name)
                    for i in range(len(lvalues)):
                        hstr={"d_id":d_id,
                            "spec_id":i,
                            "specialty":h_name}
                        data_hold.append(hstr)
            if lkey=='name':
                #print('I got service name')
                h_name=lvalues

    # creating dataframe
    specialty_df=pd.DataFrame(data_hold)
    filter=specialty_df['spec_id']==0
    new_specialty_df=specialty_df.where(filter)
    new_specialty_df.dropna(inplace=True)


    return new_specialty_df


def get_org_demographics(jvalue,d_id):
    h_resource=False
    h_name=''
    h_resourcetype=''
    d_name=''
    d_gender=''
    d_lob=''
    d_str=''
    data_hold=[]
    data_id_hold=[]
    for nkey,nvalues in jvalue.items():
        for lkey,lvalues in nvalues.items():
            #print(lkey)
            if lkey=='resourceType':
                #print('did i get resourcetype')
                h_resourcetype=lvalues
                #print(lvalues)
    #             if lvalues=='Practitioner':
    #                 #print(h_name)
    #                 for i in range(len(lvalues)):

    #                     hstr={"d_id":d_id,
    #                         "name":i,
    #                         "specialty":h_name}
    #                     data_hold.append(hstr)
            if lkey=='name' and h_resourcetype=='Organization':
                # print(lvalues)
                # print('got here')
                # print(h_resourcetype)
                # print(str(lvalues).find('given'))
                if str(lvalues).find('given')!=-1:
                    d_name='{0} {1}'.format(lvalues[0]['given'][0],lvalues[0]['family'])
                else:
                    d_name='{0}'.format(lvalues)
                #print(d_name)
    #             #print('I got service name')
    #             h_name=lvalues
            if lkey=='gender' and h_resourcetype=='Practitioner':
                # print(lvalues)
                # print('got here again')
                # print(h_resourcetype)
                d_gender='{0}'.format(str(lvalues).upper())

            if lkey=='name' and h_resourcetype=='Practitioner':
                # print(lvalues)
                # print('got here')
                # print(h_resourcetype)
                if str(lvalues).find('given')==-1:
                    d_lob='{0}'.format(str(lvalues).upper())
                else:
                    d_lob=''

            if lkey=='id' and lvalues==d_id:
                dstr={"d_id":d_id,
                        "name":d_name,
                        "gender":d_gender,
                        "lob":d_lob}
                data_hold.append(dstr)

            # if lkey=='alias' and h_resourcetype=='Organization':
            #     print(lvalues)
            #     print('trying for lob')
            #     print(h_resourcetype)
            #     d_lob='{0}'.format(str(lvalues[0]).upper())
            #     print(d_lob)



    # creating dataframe
    demo_df=pd.DataFrame(data_hold)

    return demo_df

def get_org_address(jvalue,d_id):
    h_resource=False
    h_name=''
    h_resourcetype=''
    d_address=''
    d_gender=''
    d_lob=''
    n=-1
    data_hold=[]
    data_id_hold=[]
    for nkey,nvalues in jvalue.items():
        for lkey,lvalues in nvalues.items():
            #print(lkey)
            if lkey=='resourceType':
                #print('did i get resourcetype')
                h_resourcetype=lvalues
                #print(lvalues)
    #             if lvalues=='Practitioner':
    #                 #print(h_name)
    #                 for i in range(len(lvalues)):

    #                     hstr={"d_id":d_id,
    #                         "name":i,
    #                         "specialty":h_name}
    #                     data_hold.append(hstr)
            if lkey=='address' and h_resourcetype=='Location':
                # print(lvalues)
                # print(lvalues['line'])
                # print('got here')
                # print(h_resourcetype)
                d_address='{0} {1}, {2} {3}'.format(str(lvalues['line'][0]).strip(),str(lvalues['city']).strip(),lvalues['state'],str(lvalues['postalCode'])[0:5]+'-'+str(lvalues['postalCode'])[5:])
                n+=1
                dstr={"d_id":d_id,
                    "address":d_address,
                    "addr_id":n}
                data_hold.append(dstr)



   # creating dataframe
    address_df=pd.DataFrame(data_hold)

    return address_df

def get_org_phone(jvalue,d_id):
    h_resource=False
    h_name=''
    h_resourcetype=''
    d_phone=''
    d_gender=''
    d_lob=''
    n=-1
    data_hold=[]
    data_id_hold=[]
    for nkey,nvalues in jvalue.items():
        for lkey,lvalues in nvalues.items():
            #print(lkey)
            if lkey=='resourceType':
                #print('did i get resourcetype')
                h_resourcetype=lvalues

            if lkey=='telecom' and h_resourcetype=='Location':
                # print(lvalues)
                # print(lvalues[0]['value'])
                # print('got here')
                # print(h_resourcetype)
                d_phone='{0}'.format(lvalues[0]['value'])
                n+=1
                dstr={"d_id":d_id,
                    "phone":d_phone,
                    "addr_id":n}
                data_hold.append(dstr)



   # creating dataframe
    phone_df=pd.DataFrame(data_hold)

    return phone_df

def get_api_demographic(practitionerid):
    CALL_PRACTITIONER_ID='/Practitioner?id={providerid}'
    data_hold=[]
    d_name=''
    gender_name=''
    specialty=''
    prov_id=''
    response=requests.get(ENDPOINT+CALL_PRACTITIONER_ID.format(providerid=practitionerid))
    if response.status_code==200:
        for key,values in response.json().items():
            #print(key)
            #print(values)
            if key=='entry':
                t=pd.DataFrame(values)
                if response.text.find('"resource":')!=-1:
                    for akey,avalue in t['resource'].items():
                        #print(avalue)
                        for nkey,nvalue in avalue.items():
                            if nkey=='name':
                                d_name='{0} {1}'.format(nvalue[0]['given'][0],nvalue[0]['family'])

                            if nkey=='gender':
                                gender_name='{0}'.format(nvalue).upper()

                            # if nkey=='qualification':
                            #     specialty='{0}'.format(str(nvalue[0]['code']['coding'][0]['display']).strip())
                            if nkey=='identifier':

                                print('provider id')
                                print(nvalue)
                                for pp in range(len(nvalue)):
                                    print('checking provider id info')
                                    if str(nvalue[pp]).find('PROVIDER_ID')!=-1:
                                        print('found provider id')
                                        print(nvalue[pp]['value'])
                                        prov_id=nvalue[pp]['value']




                        jstr={"d_id":practitionerid,
                                "name":d_name,
                                "gender":gender_name,
                                "provider_id":prov_id}

                        data_hold.append(jstr)
        #creating dataframe
        demo_df=pd.DataFrame(data_hold)
        return demo_df

    else:

        #creating dataframe
        return {"data":[]}

def get_api_location(practitionerid):
    CALL_PRACTITIONER_ID='/Location?_has:PractitionerRole:location:practitioner={providerid}'
    data_hold=[]
    d_address=''
    d_phone=''

    response=requests.get(ENDPOINT+CALL_PRACTITIONER_ID.format(providerid=practitionerid))
    if response.status_code==200:
        for key,values in response.json().items():
            #print(key)
            #print(values)
            if key=='entry':
                t=pd.DataFrame(values)
                if response.text.find('"resource":')!=-1:
                    for akey,avalue in t['resource'].items():
                        #print(avalue)
                        for nkey,nvalue in avalue.items():
                            if nkey=='address':
                                if nvalue!=[]:
                                    d_address='{0} {1}, {2} {3}'.format(str(nvalue['line'][0]).strip(),str(nvalue['city']).strip(),nvalue['state'],str(nvalue['postalCode'])[0:5]+'-'+str(nvalue['postalCode'])[5:])

                                else:
                                    d_address='{0} {1} {2} {3}'.format('','','','')

                            if nkey=='telecom':
                                d_phone='{0}'.format(nvalue[0]['value'])




                        jstr={"d_id":practitionerid,
                                "address":d_address,
                                "phone":d_phone}

                        data_hold.append(jstr)
                else:
                    jstr={"d_id":practitionerid,
                                "address":'',
                                "phone":''}

                    data_hold.append(jstr)
        #creating dataframe
        demo_df=pd.DataFrame(data_hold)
        if data_hold!=[]:
            new_demo_df=demo_df.drop_duplicates()
            return new_demo_df
        else:
            return demo_df

    else:

        #creating dataframe
        return {"data":[]}






def get_api_organization(practitionerid):
    CALL_PRACTITIONER_ID='/Organization?_has:PractitionerRole:network:practitioner={providerid}'
    data_hold=[]
    d_lob_name=''
    d_lob=''

    response=requests.get(ENDPOINT+CALL_PRACTITIONER_ID.format(providerid=practitionerid))
    if response.status_code==200:
        for key,values in response.json().items():
            #print(key)
            #print(values)
            if key=='entry':
                t=pd.DataFrame(values)
                if response.text.find('"resource":')!=-1:
                    for akey,avalue in t['resource'].items():
                        #print(avalue)
                        for nkey,nvalue in avalue.items():
                            if nkey=='name':
                                if nvalue!=[]:
                                    d_lob_name='{0}'.format(str(nvalue).strip())

                                else:
                                    d_lob_name='{0}'.format('')

                            if nkey=='alias':
                                d_lob='{0}'.format(nvalue[0])




                        jstr={"d_id":practitionerid,
                                "lob":d_lob,
                                "lobname":d_lob_name}

                        data_hold.append(jstr)
                else:
                    jstr={"d_id":practitionerid,
                                "lob":'',
                                "lobname":''}

                    data_hold.append(jstr)
        #creating dataframe
        demo_df=pd.DataFrame(data_hold)
        return demo_df

    else:

        #creating dataframe
        return {"data":[]}


def get_api_specialty(practitionerid):
    #CALL_PRACTITIONER_ID='/HealthcareService?_has:PractitionerRole:healthcareService:practitioner={providerid}'
    CALL_PRACTITIONER_ID='/Practitioner?id={providerid}'
    data_hold=[]
    d_specialty=''
    n=-1

    response=requests.get(ENDPOINT+CALL_PRACTITIONER_ID.format(providerid=practitionerid))
    if response.status_code==200:
        for key,values in response.json().items():
            #print(key)
            #print(values)
            if key=='entry':
                t=pd.DataFrame(values)
                if response.text.find('"resource":')!=-1:
                    for akey,avalue in t['resource'].items():
                        #print(avalue)
                        for nkey,nvalue in avalue.items():

                            if nkey=='qualification':

                                print(n)
                                if nvalue!=[]:
                                    print(len(nvalue))
                                    #d_specialty='{0}'.format(str(nvalue[0]['coding'][0]['display']).strip())
                                    for i in range(len(nvalue)):
                                        n+=1
                                        d_specialty='{0}'.format(str(nvalue[n]['code']['coding'][0]['display']).strip())
                                        print(d_specialty)
                                        jstr={"d_id":practitionerid,
                                        "specialty":d_specialty}

                                        data_hold.append(jstr)

                                else:
                                    d_specialty='{0}'.format('')
                                    jstr={"d_id":practitionerid,
                                    "specialty":d_specialty}

                                    data_hold.append(jstr)







                else:
                    jstr={"d_id":practitionerid,
                                "specialty":''}

                    data_hold.append(jstr)
        #creating dataframe
        demo_df=pd.DataFrame(data_hold)
        if data_hold!=[]:
            new_demo_df=demo_df.drop_duplicates()
            return new_demo_df
        else:
            return demo_df

    else:

        #creating dataframe
        return {"data":[]}


def get_all_providers():
    response=requests.get(ENDPOINT+CALL_PROVIDER_ALL)
    if response.status_code==200:
        return response.json()
    else:
        return {"data:'NO DATA FOUND'"}

def get_providers(provider,whichsearch):
    print(whichsearch)
    if whichsearch=='Organization':
        return get_providers_for_organization(provider)
        response=requests.get(ENDPOINT+CALL_ORGANIZATION.format(provider=provider))
        if response.status_code==200:
            # tp=pd.read_json(json.dumps(response.json()),orient='columns',lines=True)
            # print(tp['entry'])
            data_hold=[]
            new_data_hold=[]
            gender='NA'
            responses=response.json()
            print(response.text.find('"resource":'))
            #print(response.text)
            if response.text.find('"resource":')!=-1:
                for key,values in response.json().items():
                    #print(key)

                    if key=='entry':

                        t=pd.DataFrame(values)
                        print(t.head())
                        print(t['resource'])
                        new_org=get_api_organization_id(t['resource'])
                        print('checking new org id')
                        print(new_org)
                        for nkey,nvalues in new_org.iterrows():

                            #print(nkey)
                            #print(nvalues)
                            # need function to get ID with Demographics,Address,Phone
                            #print(get_demographics(nvalues,whichsearch))
                            #print(get_address(nvalues,whichsearch))
                            #print(get_phone(nvalues,whichsearch))
                            # dem_df=get_demographics(nvalues,whichsearch)
                            # addr_df=get_address(nvalues,whichsearch)
                            # phone_df=get_phone(nvalues,whichsearch)

                            new_org_dem=get_api_org_demographics(nvalues['d_id'])
                            print(new_org_dem)

                            new_org_address=get_api_org_location(nvalues['d_id'])
                            print(new_org_address)

                            new_org_phone=get_api_org_phone(nvalues['d_id'])
                            print(new_org_phone)


                            m1_df=pd.merge(new_org_dem,new_org_address,on='d_id')
                            m2_df=pd.merge(m1_df,new_org_phone,on=['d_id','addrid'])
                            print(m2_df)
                            new_data_hold.append(m2_df)






                    # i+=1
            if new_data_hold!=[]:
                final_df=pd.concat(new_data_hold)
                print("new df")
                print(final_df)
                result=final_df.to_json(orient='table')
                print(result)
                print("old return")
                return result
            else:
                return {"data":new_data_hold}

            #return {"data":[]} # for testing
        else:
            return {"data":[]}
    else:
        #response=requests.get(ENDPOINT+CALL_PROVIDER_NAME.format(provider=provider))
        return get_providers_for_practitioner(provider)
        response=requests.get(ENDPOINT+CALL_PROVIDER_NAME.format(provider=provider))
        if response.status_code==200:

            #print(response.text)
            h_resource=False
            h_name=''
            h_resourcetype=''
            new_id=pd.DataFrame([])
            new_specialty=[]
            new_org_data_hold=[]
            for key,values in response.json().items():
                #print(key)
                #print(values)
                if key=='entry':
                    t=pd.DataFrame(values)
                    print(t.head())
                    if t.empty==False:
                        new_id=get_practitioner_id(t['resource'])
                        print(new_id)
                    if new_id.empty==False:

                        for rkey,rvalue in new_id.iterrows():
                            print(rvalue)
                            # new_specialty=get_specialty(t['resource'],rvalue['d_id'])
                            # print(new_specialty)
                            # new_demo=get_org_demographics(t['resource'],rvalue['d_id'])
                            # print(new_demo)

                            new_demo=get_api_demographic(rvalue['d_id'])
                            #print(new_demo)

                            new_address=get_api_location(rvalue['d_id'])
                            #print(new_address)

                            new_organization=get_api_organization(rvalue['d_id'])
                            #print(new_organization)

                            new_specialty=get_api_specialty(rvalue['d_id'])
                            #print(new_specialty)
                            # new_address=get_org_address(t['resource'],rvalue['d_id'])
                            # print(new_address)
                            # new_phone=get_org_phone(t['resource'],rvalue['d_id'])
                            # print(new_phone)

                            m1_df=pd.merge(new_demo,new_address,on='d_id')
                            m2_df=pd.merge(m1_df,new_organization,on='d_id')
                            m3_df=pd.merge(m2_df,new_specialty,on='d_id')
                            #print(m3_df)
                            new_org_data_hold.append(m3_df)

                    #print(new_demo)
                    #print(t['resource'])
                    # for nkey,nvalues in t['resource'].items():
                    #     print(nkey)
                    #     print(nvalues)
                    #     new_id=get_practitioner_id(nvalues)
                    #     print(new_id)
                        # for lkey,lvalues in nvalues.items():
                        #     print(lkey)
                        #     print(lvalues)
                        #     if lkey=='resourceType':
                        #         new_id=get_practitioner_id(nvalues)
                        #         print(new_id)
                        #         #print(lvalues)
                        #     # #new_specialty=get_specialty(nvalues,new_id)
                        #     #     print(new_id)
                        #     # #print(new_specialty)

            if new_org_data_hold!=[]:
                final_df=pd.concat(new_org_data_hold)
                #print("new df")
                #print(final_df)
                result=final_df.to_json(orient='table')
                print(result)
                print("old return")
                return result
            else:
                return {"data":new_org_data_hold}

        else:
            return {"data":[]}

def get_providers_for_practitioner(provider):
    t1 = time.time()
    response=requests.get(ENDPOINT+CALL_PROVIDER_NAME_FAST.format(practitionerName=provider))
    t2 = time.time()
    print("Aidbox endpoint exec time:", t2 - t1)
    new_org_data_hold=[]

    t1 = time.time()
    if response.status_code == 200:
        if len(response.json()["entry"]) < 1:
            return {"data": []}
        entry_resource = pd.DataFrame(response.json()["entry"])["resource"]

        df = pd.DataFrame.from_records(response.json()["entry"], columns=["resource"])
        df = (
            pd.json_normalize(response.json()["entry"])[["resource.resourceType", "resource.id", "resource.practitioner.id", "resource.location", "resource.network"]]
            .merge(df, left_index=True, right_index = True)
        )
        practitioner_ = df.loc[df['resource.resourceType'] == 'Practitioner']
        practitioners = get_practitioner_id(practitioner_["resource"])
        # pd.json_normalize(df[df['resource.location'].notnull()]['resource.location'].apply(pd.Series).unstack().reset_index().dropna()[0])

        for rkey,rvalue in practitioners.iterrows():
            print(rvalue)
            prct = find_entity(df, rvalue['d_id'])
            new_demo = parse_demographic(prct)
            new_address = parse_location(df, prct)
            new_organization = parse_organization(df, prct)
            new_specialty = parse_specialty(prct)

            m1_df=pd.merge(new_demo,new_address,on='d_id')
            m2_df=pd.merge(m1_df,new_organization,on='d_id')
            m3_df=pd.merge(m2_df,new_specialty,on='d_id')
            #print(m3_df)
            new_org_data_hold.append(m3_df)
        if new_org_data_hold!=[]:
            final_df=pd.concat(new_org_data_hold)
            #print("new df")
            #print(final_df)
            result=final_df.to_json(orient='table')
            print(result)
            print("old return")
            t2 = time.time()
            print("Data processing time:", t2 - t1)
            return result
        else:
            return {"data":new_org_data_hold}
    else:
        t2 = time.time()
        print("Data processing time:", t2 - t1)
        return {"data":[]}

def get_providers_for_organization(name):
    t1 = time.time()
    response = requests.get(ENDPOINT + CALL_ORGANIZATION_FAST.format(organizationName=name))
    t2 = time.time()
    print("Aidbox endpoint exec time:", t2 - t1)
    new_org_data_hold=[]

    if response.status_code == 200:
        if len(response.json()["entry"]) < 1:
            return {"data": []}

        t1 = time.time()
        df = pd.DataFrame.from_records(response.json()["entry"], columns=["resource"])
        df = (
            pd.json_normalize(response.json()["entry"])[["resource.resourceType", "resource.id", "resource.participatingOrganization.id"]]
            .merge(df, left_index=True, right_index = True)
        )

        organizations = df.loc[df['resource.id'].isin(df['resource.participatingOrganization.id'].dropna())]
        t2 = time.time()
        print("Data merge time:", t2 - t1)
        t1 = time.time()
        new_org = get_api_organization_id(organizations['resource'])

        for nkey,nvalues in new_org.iterrows():
            organization = find_entity(df, nvalues['d_id'])

            new_org_dem = parse_org_demographic(organization)
            new_org_address = parse_org_location(organization)
            new_org_phone=parse_org_phone(organization)
            m1_df=pd.merge(new_org_dem,new_org_address,on='d_id')
            m2_df=pd.merge(m1_df,new_org_phone,on=['d_id','addrid'])
            # print(m1_df)
            new_org_data_hold.append(m2_df)

        t2 = time.time()
        print("Parse time:", t2 - t1)

        if new_org_data_hold!=[]:
            t1 = time.time()
            final_df=pd.concat(new_org_data_hold)
            # print("new df")
            # print(final_df)
            result=final_df.to_json(orient='table')
            # print(result)
            # print("old return")
            t2 = time.time()
            print("assembly time:", t2 - t1)
            return result
        else:
            return {"data":new_org_data_hold}
    else:
        return {"data":[]}



def find_entity(df, uuid):
    return (df.loc[df['resource.id'] == uuid]).iloc[0]

def parse_demographic(t):
    data_hold=[]
    d_name=''
    gender_name=''
    specialty=''
    prov_id=''

    for nkey,nvalue in t['resource'].items():
        if nkey=='name':
            d_name='{0} {1}'.format(nvalue[0]['given'][0],nvalue[0]['family'])

        if nkey=='gender':
            gender_name='{0}'.format(nvalue).upper()

        # if nkey=='qualification':
        #     specialty='{0}'.format(str(nvalue[0]['code']['coding'][0]['display']).strip())
        if nkey=='identifier':

            print('provider id')
            print(nvalue)
            for pp in range(len(nvalue)):
                print('checking provider id info')
                if str(nvalue[pp]).find('PROVIDER_ID')!=-1:
                    print('found provider id')
                    print(nvalue[pp]['value'])
                    prov_id=nvalue[pp]['value']




    jstr={"d_id":t['resource.id'],
          "name":d_name,
          "gender":gender_name,
          "provider_id":prov_id}

    data_hold.append(jstr)
    #creating dataframe
    demo_df=pd.DataFrame(data_hold)
    return demo_df

def parse_location(df, practitionerid):


    pr_roles = df.loc[
        (df['resource.resourceType'] == 'PractitionerRole') & (df['resource.practitioner.id'] == practitionerid['resource.id'])]
    loc_ids = pd.json_normalize(pr_roles[pr_roles['resource.location'].notnull()]['resource.location'].apply(pd.Series).unstack().reset_index().dropna()[0])['id']
    locations = df.loc[df['resource.id'].isin(loc_ids)]
    # locations = df.loc[df['resource.id'].isin(loc_ids)]['resource']

    data_hold=[]
    d_address=''
    d_phone=''

    for akey,avalue in locations['resource'].items():
        #print(avalue)
        for nkey,nvalue in avalue.items():
            if nkey=='address':
                if nvalue!=[]:
                    d_address='{0} {1}, {2} {3}'.format(str(nvalue['line'][0]).strip(),str(nvalue['city']).strip(),nvalue['state'],str(nvalue['postalCode'])[0:5]+'-'+str(nvalue['postalCode'])[5:])

                else:
                    d_address='{0} {1} {2} {3}'.format('','','','')

            if nkey=='telecom':
                d_phone='{0}'.format(nvalue[0]['value'])




        jstr={"d_id":practitionerid['resource.id'],
              "address":d_address,
              "phone":d_phone}

        data_hold.append(jstr)
    #creating dataframe
    demo_df=pd.DataFrame(data_hold)
    if data_hold!=[]:
        new_demo_df=demo_df.drop_duplicates()
        return new_demo_df
    else:
        return demo_df

def parse_organization(df, practitionerid):

    pr_roles = df.loc[
        (df['resource.resourceType'] == 'PractitionerRole') & (df['resource.practitioner.id'] == practitionerid['resource.id'])]
    network_ids = pd.json_normalize(pr_roles[pr_roles['resource.network'].notnull()]['resource.network'].apply(pd.Series).unstack().reset_index().dropna()[0])['id']
    networks = df.loc[df['resource.id'].isin(network_ids)]


    data_hold=[]
    d_lob_name=''
    d_lob=''

    if len(networks) < 1:
        jstr = {"d_id": practitionerid['resource.id'],
                "lob": '',
                "lobname": ''}
        data_hold.append(jstr)
    else:
        for akey, avalue in networks['resource'].items():
            # print(avalue)
            for nkey, nvalue in avalue.items():
                if nkey == 'name':
                    if nvalue != []:
                        d_lob_name = '{0}'.format(str(nvalue).strip())
                    else:
                        d_lob_name = '{0}'.format('')
                if nkey == 'alias':
                    d_lob = '{0}'.format(nvalue[0])
            jstr = {"d_id": practitionerid['resource.id'],
                    "lob": d_lob,
                    "lobname": d_lob_name}

            data_hold.append(jstr)
    # creating dataframe
    demo_df = pd.DataFrame(data_hold)
    return demo_df

def parse_specialty(practitioner):
    data_hold=[]
    d_specialty=''
    n=-1

    for nkey,nvalue in practitioner['resource'].items():
        if nkey=='qualification':
            print(n)
            if nvalue!=[]:
                print(len(nvalue))
                #d_specialty='{0}'.format(str(nvalue[0]['coding'][0]['display']).strip())
                for i in range(len(nvalue)):
                    n+=1
                    d_specialty='{0}'.format(str(nvalue[n]['code']['coding'][0]['display']).strip())
                    print(d_specialty)
                    jstr={"d_id":practitioner['resource.id'],
                          "specialty":d_specialty}

                    data_hold.append(jstr)

            else:
                d_specialty='{0}'.format('')
                jstr={"d_id":practitioner['resource.id'],
                      "specialty":d_specialty}

                data_hold.append(jstr)
    #creating dataframe
    demo_df=pd.DataFrame(data_hold)
    if data_hold!=[]:
        new_demo_df=demo_df.drop_duplicates()
        return new_demo_df
    else:
        return demo_df

def parse_org_demographic(organization) :
    data_hold=[]
    d_name=''
    gender_name='NA'

    for nkey,nvalue in organization['resource'].items():
        if nkey=='name':
            d_name='{0}'.format(nvalue)

        if nkey=='gender':
            gender_name='{0}'.format('NA')

        # if nkey=='qualification':
        #     specialty='{0}'.format(str(nvalue[0]['code']['coding'][0]['display']).strip())

    jstr={"d_id":organization['resource.id'],
          "name":d_name,
          "gender":gender_name}

    data_hold.append(jstr)
    demo_df=pd.DataFrame(data_hold)
    return demo_df

def parse_org_location(organization) :
    data_hold=[]
    d_address=''
    d_phone=''
    n=-1

    for nkey,nvalue in organization['resource'].items():
        if nkey=='address':
            if nvalue!=[]:

                for i in range(len(nvalue)):
                    n+=1
                    if str(nvalue[n]).find('postalCode')!=-1:
                        d_address='{0} {1}, {2} {3}'.format(str(nvalue[n]['line'][0]).strip(),str(nvalue[n]['city']).strip(),nvalue[n]['state'],str(nvalue[n]['postalCode'])[0:5]+'-'+str(nvalue[n]['postalCode'])[5:])
                    else:
                        d_address='{0} {1}, {2} {3}'.format(str(nvalue[n]['line'][0]).strip(),str(nvalue[n]['city']).strip(),nvalue[n]['state'],'')
                    jstr={"d_id": organization['resource.id'],
                          "addrid":n,
                          "address":d_address}

                    data_hold.append(jstr)

            else:
                d_address='{0} {1} {2} {3}'.format('','','','')
                jstr={"d_id": organization['resource.id'],
                      "addrid":0,
                      "address":d_address}

                data_hold.append(jstr)

    #creating dataframe
    demo_df=pd.DataFrame(data_hold)
    if data_hold!=[]:
        new_demo_df=demo_df.drop_duplicates()
        return new_demo_df
    else:
        return demo_df

def parse_org_phone(organization) :
    data_hold=[]
    d_phone=''
    nd=-1

    for nkey,nvalue in organization['resource'].items():
        if nkey=='telecom':
            print(nvalue)
            if nvalue!=[]:
                for d in range(len(nvalue)):
                    nd+=1
                    d_phone='{0}'.format(nvalue[nd]['value'])

                    jstr={"d_id":organization['resource.id'],
                          "addrid":nd,
                          "phone":d_phone}

                    data_hold.append(jstr)
            else:
                jstr={"d_id":organization['resource.id'],
                      "addrid":0,
                      "phone":d_phone}

                data_hold.append(jstr)
    #creating dataframe
    demo_df=pd.DataFrame(data_hold)
    if data_hold!=[]:
        new_demo_df=demo_df.drop_duplicates()
        return new_demo_df
    else:
        return demo_df

