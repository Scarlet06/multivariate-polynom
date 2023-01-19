import examples

#print multivariate polynomial
examples.shower(examples.m0)
examples.shower(examples.m_random_dict)

#check operations between multivariate polynomial
examples.operator(examples.m_dict_integrals,examples.m_random_unkn)
examples.operator(examples.m_text,18.7)

#check applications on multivariate polynomial
examples.applicator(examples.m_dict,-2,6)

print("\n","-"*50,"\n")
#print complex multivariate polynomial
examples.shower(examples.cm_text_integ)

#check operations between complex multivariate polynomial
examples.operator(examples.cm_dict,examples.cm_random_dict)
examples.operator(examples.cm1,18.7)

#check applications on complex multivariate polynomial
examples.applicator(examples.cm_text_unkn,-2,6)