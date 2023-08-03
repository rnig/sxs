  <Customer CustomerSequenceNumber="{{ CustomerSequenceNumber }}" CustomerBankIdentification="{{ CustomerBankIdentification }}">
    <CustomerIdentification>
      {{ EntityIdentification }}
    </CustomerIdentification>
    <CustomerActions>
      <{{ Mode }}Action>
        <Contracts>
          <Contract RelationSequenceNumber="{{ RelationSequenceNumber }}">
            <ContractTypeName>
		      <{{ ContractTypeName }}/>
		    </ContractTypeName>
		    <Customer{{ Action }}>{{ ActionDate }}</Customer{{ Action }}>
           </Contract>
         </Contracts>
       </{{ mode }}Action>
     </CustomerActions>
  </Customer>