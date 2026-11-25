<script setup>
import Footer from '@/components/Footer.vue';
import Header from '@/components/Header.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Form } from 'vee-validate';


let route = useRoute();
let dados = ref({});
let botao = ref('block');
let preloader = ref('none');


onMounted(async () => {
    let resposta = await fetch(import.meta.env.VITE_API_URL + 'receitas/' + route.params.id, 
        { headers: { 'content-type': 'application/json' } });
    if (resposta.status != 200) {
        window.location = "/error";
    }
    dados.value = await resposta.json();
});
let enviar=async ()=>
{
    botao.value="none";
    preloader.value="block";
    let file = document.querySelector("input[type=file]").files[0];
    let formData =new FormData();
    formData.append('foto', file);
    formData.append('id', route.params.id);
    try {
        let resp = await fetch(`${import.meta.env.VITE_API_URL}receitas/editar/foto`, 
        {
            method: 'POST',
            body:formData,
            headers:{'Authorization': `Bearer ${localStorage.getItem('receitas_flaites_token')}`}
        })
        if(resp.status==200)
        {
            alert("Editado com sucesso");
            window.location='/painel/';
        }
    } catch {
        alert("Ocorreu um erro inesperado");
        window.location="/painel/editar/"+route.params.id;
    }
};
</script>

<template>

    <Header />
    <div className="breadcumb-area bg-img bg-overlay" style="background-image: url(img/bg-img/breadcumb6.jpg)">
        <div className="container h-100">
            <div className="row h-100 align-items-center">
                <div className="col-12">
                    <div className="breadcumb-text text-center">
                        <h2>Editar foto: {{ dados.data?.nome }}</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div className="contact-area section-padding-0-80">
        <div className="container">
            <div className="row">
                <div className="col-12">
                    <div className="section-heading">
                        <h3>Editar foto: {{ dados.data?.nome }}</h3>
                    </div>
                </div>
            </div>

            <div className="row">
                <div className="col-8">
                    <div className="contact-form-area">
                        <Form @submit="enviar()">
                            <div class="row">
                                <div class="col-12 col-lg-12">
                                    <img :src="dados.data?.imagem" style="width: 200px;" />
                                    <hr/>
                                </div>
                                <div class="col-12 col-lg-12">
                                    <input type="file" class="form-control" id="foto" placeholder="Foto" />
                                </div>


                                <div class="col-12 text-center" :style="'display:' + botao">
                                    <button class="btn delicious-btn mt-30" type="submit" title="Enviar">Enviar</button>
                                </div>
                                <div class="col-12 text-center" :style="`display:${preloader}`">
                                    <img src="/img/img/load.gif" alt="" />
                                </div>
                            </div>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <Footer />
</template>