from bb_wrapper.wrapper.bb import BaseBBWrapper


wrapper = BaseBBWrapper()
response = wrapper.authenticate()

print(response.data)
