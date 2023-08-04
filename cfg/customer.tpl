  <Customer CustomerSequenceNumber="$CustomerSequenceNumber" CustomerBankIdentification="$CustomerBankIdentification">
    <CustomerIdentification>
      $EntityIdentification
    </CustomerIdentification>
    <CustomerActions>
      <$ModeAction>
        <Contracts>
          <Contract RelationSequenceNumber="$RelationSequenceNumber">
            <ContractTypeName>
		      <$ContractTypeName/>
		    </ContractTypeName>
		    <Customer$Action>$ActionDate</Customer$Action>
           </Contract>
         </Contracts>
       </$Modeaction>
     </CustomerActions>
  </Customer>