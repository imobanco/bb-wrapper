from imobanco_bb.wrapper.bb import BaseBBWrapper


wrapper = BaseBBWrapper()
response = wrapper.authenticate()

print(response.data)
