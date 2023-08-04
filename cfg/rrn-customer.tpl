  <Customer CustomerSequenceNumber="$CustomerSequenceNumber" CustomerBankIdentification="$CustomerBankIdentification">
    <CustomerIdentification>
	<NaturalPersonId>
          <RRNIdentification>$RRNIdentification</RRNIdentification>
	</NaturalPersonId>
    </CustomerIdentification>
    <CustomerActions>
      <$ModeAction>
        <Contracts>
          <Contract RelationSequenceNumber="$RelationSequenceNumber">
            <ContractTypeName>
	      <$ContractTypeName/>
	    </ContractTypeName>
	    <Customer$Action>$Date</Customer$Action>
           </Contract>
         </Contracts>
       </$modeAction>
     </CustomerActions>
  </Customer>