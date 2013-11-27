% rebase layout route_prefix=route
<div class="container">
<h1>Notes</h1>
<form action="/new">
      <input class="btn btn-primary" type="submit" value="New Note">
</form>
%if new == True:
<form role="form" action="/new" method="POST">
<div class="form-group">
     <label for="title">Title:</label>
     <input type="title" class="form-control" id="title" placeholder="Enter title" name="title">
</div>
<div class="form-group">
     <label for="content">Note:</label>
     <input type="content" class="form-control" id="content" placeholder="Enter note" name="content">
</div>
<input class="btn btn-primary" type="submit" value="save" name="save">
</form>
%end
<table class="table table-condensed">
  <tr>
    <th>Id</th>
    <th>Title</th>
    <th>Note</th>
    <th>Action</th>
  </tr>
%for row in rows:
  <tr>
    <td>{{row.get('id')}}</td>
    <td>{{row.get('title')}}</td>
    <td>{{row.get('content')}}</td>
    <td><form action="/delete/{{row.get('id')}}">
               <input class="btn btn-danger btn-xs" type="submit" value="Delete Note">
         </form>
    </td>
  </tr>
%end
</table>
</div>
