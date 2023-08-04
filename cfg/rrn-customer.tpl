  <Customer CustomerSequenceNumber="$CustomerSequenceNumber" CustomerBankIdentification="$CustomerBankIdentification">
    <CustomerIdentification>
	<NaturalPersonId>
          <RRNIdentification>$RRNIdentification</RRNIdentification>
	</NaturalPersonId>
    </CustomerIdentification>
    <CustomerActions>
      <$Modus>
        <Contracts>
          <Contract RelationSequenceNumber="$RelationSequenceNumber">
            <ContractTypeName>
	      <$ContractTypeName/>
	    </ContractTypeName>
	    <Customer$Action>$Date</Customer$Action>
           </Contract>
         </Contracts>
       </$Modus>
     </CustomerActions>
  </Customer>
