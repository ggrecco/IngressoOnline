% rebase('./view/base.tpl',title='Meu carrinho')
% subtotal = 0
% total = 0
<div class="row">
    <div class="col-md-3"></div>
        <div class="col-md-6">
                    <h2 class="text-center">Meu carrinho:</h2>
         	<hr/>
        </div>
    </div>
	<div class="row" style="margin-top:10px;">
		<div class="col-md-3"></div>
		<div class="col-md-6">
			%if len(dado) != 0:
			<div class="table-responsive">
				<table class="table">
					<thead class="thead-dark">
						<tr>						
							<th scope="col">Titulo</th>
							<th scope="col">Quantidade</th>
							<th scope="col">Tipo</th>
							<th scope="col">Subtotal</th>
							<th scope="col"></th>
						</tr>
					</thead>
					<tbody>
						%for item in dado:
						<tr>							
							<td scope="col">{{item[2]}}</td>
							<td scope="col">{{item[1]}}</td>
							<td scope="col">{{item[4]}}</td>
							%subtotal = int(item[1]) * float(item[5].replace(',','.'))
							%total += subtotal
							<td scope="col">R$ {{subtotal}}</td>
							<td>
								<a href="/carrinho/delete/{{item[0]}}"><img class="icones-image" title="Excluir" src="/static/img/minus.png"/></a>
							</td>
						</tr>
						%end
						<tr>
							<td scope="col" colspan="5" class="text-right">Total:{{total}}</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div class="col-md-3"></div>
			%else:
				<div class="alert alert-info" role="alert">
			  		Carrinho vazio
				</div>
			%end
		</div>
	</div>