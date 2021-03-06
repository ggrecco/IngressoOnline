% rebase('view/base.tpl', title='Criar evento')
<form class="form-horizontal" role="form" method="POST" action="/evento/edit/{{dado[0]}}">
            <div class="row">
                <div class="col-md-12">
                    <h2 class="text-center">Criar evento:</h2>
                    <hr/>
                </div>
            </div>
    <div class="row">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <div class="form-group has-danger">
                        <label>Titulo</label>
                        <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                            <input type="text" name="titulo" class="form-control" value="{{dado[1]}}" />
                        </div>
                    </div>
                </div>
                <div class="col-md-3"></div>
            </div>
            <div class="row">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Categoria</label>
                        <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                            <select class="form-control" name="categoria_id">
                                <option value="{{dado[3]}}">{{dado[4]}}</option>
                                    %for item in categoria:
                                        %if item[0] != dado[3] and item[1] != dado[4]:
                                            <option value="{{item[0]}}">{{item[1]}}</option>
                                        %end
                                    %end
                            </select>
                        </div>
                    </div>
                </div>
                <div class="col-md-3"></div>
            </div>
            <div class="row">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Descrição</label>
                        <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                            <textarea name="descricao" class="form-control">{{dado[2]}}</textarea>   
                        </div>
                    </div>
                </div>
                <div class="col-md-3"></div>
            </div>
            <div class="row">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Endereço/Numero</label>
                        <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                            <input type="text" name="endereco" class="form-control" value="{{dado[5]}}" />   
                            <input type="number" name="numero" style="width:100px;" value="{{dado[6]}}"/>
                        </div>
                    </div>
                </div>
                <div class="col-md-3"></div>
            </div>
            <div class="row">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Cidade</label>
                        <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                            <select name="cidade_id" class="form-control text-left">
                                <option value="{{dado[9]}}">{{dado[11]}} | {{dado[10]}}</option>     
                                %for item in cidade:
                                    %if item[0] != dado[9] and item[1] != dado[10]:
                                        <option value="{{item[0]}}">{{item[2]}} | {{item[1]}}</option>
                                    %end
                                %end
                            </select>
                        </div>
                    </div>
                </div>
                <div class="col-md-3"></div>
            </div>
            <div class="row">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Bairro</label>
                        <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                            <input type="text" name="bairro" class="form-control" value="{{dado[7]}}" />  
                        </div>
                    </div>
                </div>
                <div class="col-md-3"></div>
            </div>
            <div class="row">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Telefone</label>
                        <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                            <input type="text" name="telefone" class="form-control" value="{{dado[8]}}" /> 
                        </div>
                    </div>
                </div>
                <div class="col-md-3"></div>
            </div>
            <div class="row" style="padding-top: 1rem">
                <div class="col-md-3"></div>
                <div class="col-md-6">
                    <a href="#" class="btn btn-secondary btn-sm" onclick="window.history.go(-1)">Cancelar</a>
                    <button class="btn float-md-right btn-sm btn-success">Salvar</button>
                </div>
                <div class="col-md-3"></div>
            </div>
    </div>                    
 </form>