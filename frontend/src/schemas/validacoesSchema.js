import * as yup from 'yup'

export const contatoSchema = yup.object(
    {
        nome: yup.string().required("O campo nome é obrigatório"),
        email: yup.string().required("O campo email é obrigatório").email("O email inserido não é válido"),
        telefone: yup.string().required("O campo telefone é obrigatório"),
        mensagem: yup.string().required("O campo mensagem é obrigatório")
    }
);

export const cadastroSchema = yup.object(
    {
        nome: yup.string().required("O campo nome é obrigatório"),
        email: yup.string().required("O campo email é obrigatório").email("O email inserido não é válido"),
        password: yup.string().required("O campo senha é obrigatório"),
    }
); 

export const loginSchema = yup.object(
    {
        email: yup.string().required("O campo email é obrigatório").email("O email inserido não é válido"),
        password: yup.string().required("O campo senha é obrigatório"),
    }
)

export const receitasSchema = yup.object(
    {
        categoria_id:yup.string().test({
            name:'categoria_id',
            skipAbsent: true,
            test(value, ctx){
                if(value=='0'){
                    return ctx.createError({message: 'Selecione uma categoria'})
                }
                return true;
            }
        }),
        nome: yup.string().required("O campo nome é obrigatório"),
        tempo: yup.string().required("O campo tempo é obrigatório"),
        descricao: yup.string().required("O campo descricao é obrigatório"),
    }
)

